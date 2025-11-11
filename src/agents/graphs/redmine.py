"""Redmine chatbot graph with LangGraph and Adaptive RAG."""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from src.agents.states.redmine import RedmineChatState
from src.agents.nodes.adaptive_rag import AdaptiveRAGRouter, AdaptiveRAGGrader
from src.tools.redmine import redmine_tools
from src.tools.base import get_web_search_tool
from src.services.redmine_metadata import metadata_loader
from src.services.redmine_vectorstore import redmine_vectorstore
from src.llms.base import BaseLLM
from src.utils.logger import app_logger


class AdaptiveRedmineChatbot:
    """
    Adaptive RAG-powered Redmine chatbot with LangGraph.
    
    Uses Adaptive RAG to intelligently route queries:
    - Redmine tools for project/issue data
    - Web search for external information
    - Direct answers for simple queries
    
    Includes self-correction via grading mechanisms.
    """
    
    def __init__(self, llm: BaseLLM):
        """
        Initialize Adaptive Redmine chatbot.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.tools = redmine_tools
        self.web_search = get_web_search_tool(max_results=3)
        
        # Add enhanced metadata-based tools
        from src.tools.redmine_enhanced import enhanced_tools
        self.tools = self.tools + enhanced_tools
        
        # Add vector-based semantic search tools
        from src.tools.redmine_vector import vector_tools
        self.tools = self.tools + vector_tools
        self.vector_tools = vector_tools  # Keep separate reference
        
        # Adaptive RAG components (disabled for performance)
        # self.router = AdaptiveRAGRouter(llm)
        # self.grader = AdaptiveRAGGrader(llm)
        
        # Bind tools to LLM with strict parameter handling
        self.llm_with_tools = self.llm.get_client().bind_tools(
            self.tools,
            tool_choice="auto"
        )
        
        # Cache system message for performance
        self._cached_system_message = None
        
        self.graph = self._build_graph()
        total_tools = len(self.tools)
        app_logger.info(f"Initialized AdaptiveRedmineChatbot with {total_tools} tools "
                       f"(8 original + {len(enhanced_tools)} enhanced + {len(vector_tools)} vector)")
    
    def _create_system_message(self) -> SystemMessage:
        """Create cached system message for Redmine assistant (lightweight version)."""
        
        if self._cached_system_message is not None:
            return self._cached_system_message
        
        # Lightweight metadata context (only counts, not full details)
        num_projects = len(metadata_loader.projects)
        num_statuses = len(metadata_loader.statuses)
        num_priorities = len(metadata_loader.priorities)
        
        base_prompt = f"""You are an intelligent Redmine assistant with tool access.

You have access to {num_projects} projects, {num_statuses} statuses, {num_priorities} priorities, and various Redmine tools.

**Key Tools Available:**
- get_redmine_projects: List all projects
- get_redmine_issues: Get issues for a project
- get_redmine_issue_details: Get specific issue details
- search_redmine_issues: Search issues by query
- search_redmine_metadata: Search projects/issues semantically
- create_redmine_issue: Create new issues
- update_redmine_issue: Update existing issues

**Guidelines:**
1. When asked about projects, use get_redmine_projects first
2. For issues in a specific project, find project ID then use get_redmine_issues
3. For searching across all projects, use search_redmine_issues
4. Always return concise, helpful responses
5. Use tools efficiently - avoid unnecessary calls

Be direct and helpful. Use tools to fetch real-time data."""

        self._cached_system_message = SystemMessage(content=base_prompt)
        return self._cached_system_message
    
    def _chatbot_node(self, state: RedmineChatState) -> RedmineChatState:
        """
        Main chatbot node that processes messages and decides actions.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with AI response
        """
        # Add system message only on first turn
        messages = state["messages"]
        if len(messages) == 1 or not any(isinstance(m, SystemMessage) for m in messages):
            messages = [self._create_system_message()] + messages
        
        # Get response from LLM with tools (fast mode)
        response = self.llm_with_tools.invoke(messages, config={"max_tokens": 2048})
        
        return {
            **state,
            "messages": [response]
        }
    
    def _should_continue(self, state: RedmineChatState):
        """
        Determine if we should continue to tools or end.
        
        Args:
            state: Current state
            
        Returns:
            "tools" if tool calls present, END otherwise
        """
        last_message = state["messages"][-1]
        
        # Check if the last message has tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        return END
    
    def _build_graph(self) -> StateGraph:
        """
        Build the chatbot workflow graph.
        
        Flow:
        1. User message → Chatbot (decides to use tools or respond)
        2. If tools needed → Execute tools → Back to chatbot
        3. If no tools → Generate response → End
        
        Returns:
            Compiled StateGraph
        """
        # Create graph
        workflow = StateGraph(RedmineChatState)
        
        # Add nodes
        workflow.add_node("chatbot", self._chatbot_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Set entry point
        workflow.set_entry_point("chatbot")
        
        # Add conditional edges using our custom function
        workflow.add_conditional_edges(
            "chatbot",
            self._should_continue,
            {
                "tools": "tools",
                END: END
            }
        )
        
        # After tools execute, go back to chatbot
        workflow.add_edge("tools", "chatbot")
        
        app_logger.info("Built Redmine chatbot workflow graph")
        
        return workflow.compile()
    
    def chat(self, message: str, conversation_id: str, state: RedmineChatState | None = None) -> RedmineChatState:
        """
        Process a chat message synchronously.
        
        Args:
            message: User message
            conversation_id: Conversation identifier
            state: Optional previous state to continue conversation
            
        Returns:
            Updated state with response
        """
        if state is None:
            state = {
                "messages": [],
                "conversation_id": conversation_id,
                "current_project_id": None,
                "current_issue_id": None
            }
        
        # Add user message
        state["messages"].append(HumanMessage(content=message))
        
        # Run graph
        result = self.graph.invoke(state)
        
        return result
    
    async def achat(
        self,
        message: str,
        conversation_id: str,
        state: RedmineChatState | None = None
    ) -> RedmineChatState:
        """
        Process a chat message asynchronously.
        
        Args:
            message: User message
            conversation_id: Conversation identifier
            state: Optional previous state to continue conversation
            
        Returns:
            Updated state with response
        """
        if state is None:
            state = {
                "messages": [],
                "conversation_id": conversation_id,
                "current_project_id": None,
                "current_issue_id": None
            }
        
        # Add user message
        state["messages"].append(HumanMessage(content=message))
        
        # Run graph asynchronously
        result = await self.graph.ainvoke(state)
        
        return result



# Backward compatibility alias
RedmineChatbotGraph = AdaptiveRedmineChatbot
