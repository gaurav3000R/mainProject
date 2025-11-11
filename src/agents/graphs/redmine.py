"""Redmine chatbot graph with LangGraph and Adaptive RAG."""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from src.agents.states.redmine import RedmineChatState
from src.agents.nodes.adaptive_rag import AdaptiveRAGRouter, AdaptiveRAGGrader
from src.tools.redmine import redmine_tools
from src.tools.base import get_web_search_tool
from src.services.redmine_metadata import metadata_loader
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
        
        # Adaptive RAG components
        self.router = AdaptiveRAGRouter(llm)
        self.grader = AdaptiveRAGGrader(llm)
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.get_client().bind_tools(self.tools)
        
        self.graph = self._build_graph()
        app_logger.info(f"Initialized AdaptiveRedmineChatbot with {len(self.tools)} tools (incl. {len(enhanced_tools)} enhanced)")
    
    def _create_system_message(self) -> SystemMessage:
        """Create system message for Redmine assistant with Adaptive RAG and metadata context."""
        
        # Get metadata context
        metadata_context = metadata_loader.get_metadata_summary()
        
        base_prompt = """You are an intelligent Redmine assistant with Adaptive RAG capabilities.

You have access to:
- **Redmine Tools**: Direct access to projects, issues, time entries, and metadata
- **Web Search**: For external information and general knowledge
- **Your Knowledge**: For simple queries and conversational responses

**Current Redmine Instance Information:**
{metadata_context}

Capabilities:
- View and manage projects and issues
- Create and update issues
- Search and filter data
- Access time entries and metadata
- Provide helpful information

**Important Guidelines:**
1. Use EXACT project names and IDs from the list above
2. Reference actual statuses, priorities, and trackers available
3. When users mention a project name, find its ID from the list
4. For issue IDs, use numeric values only (e.g., "123", not "Project Name")
5. Always verify project/status/priority names against available options

**Examples:**
- "Show me Ni-kshay Setu Revamp issues" → Use project ID 37
- "What projects do I have?" → List the {num_projects} projects above
- "Change status to closed" → Use status ID from available statuses

Be conversational, helpful, and accurate. When using tools, explain what you found.
When information is missing or unclear, ask for clarification."""

        return SystemMessage(
            content=base_prompt.format(
                metadata_context=metadata_context,
                num_projects=len(metadata_loader.projects)
            )
        )
    
    def _chatbot_node(self, state: RedmineChatState) -> RedmineChatState:
        """
        Main chatbot node that processes messages and decides actions.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with AI response
        """
        # Add system message if this is the first message
        messages = state["messages"]
        if len(messages) == 1 or not any(isinstance(m, SystemMessage) for m in messages):
            messages = [self._create_system_message()] + messages
        
        # Get response from LLM with tools
        response = self.llm_with_tools.invoke(messages)
        
        return {
            **state,
            "messages": [response]  # Just add the new response
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
