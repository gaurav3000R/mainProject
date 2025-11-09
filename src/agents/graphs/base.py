"""Graph builders for different agent workflows."""
from typing import Optional
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.agents.states.base import ChatbotState, ResearchState, WriterState
from src.agents.nodes.base import ChatbotNode, ResearchNode, WriterNode
from src.llms.base import BaseLLM
from src.tools.base import get_web_search_tool, create_tool_node, get_available_tools
from src.core.exceptions import GraphException
from src.utils.logger import app_logger


class ChatbotGraphBuilder:
    """Builder for simple chatbot graph."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.graph = StateGraph(ChatbotState)
    
    def build(self) -> StateGraph:
        """
        Build simple chatbot graph.
        
        Returns:
            Compiled graph
        """
        app_logger.info("Building chatbot graph")
        
        try:
            chatbot_node = ChatbotNode(self.llm)
            
            self.graph.add_node("chatbot", chatbot_node.process)
            self.graph.add_edge(START, "chatbot")
            self.graph.add_edge("chatbot", END)
            
            return self.graph.compile()
        except Exception as e:
            app_logger.error(f"Failed to build chatbot graph: {str(e)}")
            raise GraphException(f"Failed to build chatbot graph: {str(e)}")


class ChatbotWithToolsGraphBuilder:
    """Builder for chatbot with tool integration."""
    
    def __init__(self, llm: BaseLLM, tool_names: Optional[list] = None):
        self.llm = llm
        self.tool_names = tool_names or ["web_search"]
        self.graph = StateGraph(ChatbotState)
    
    def build(self) -> StateGraph:
        """
        Build chatbot with tools graph.
        
        Returns:
            Compiled graph
        """
        app_logger.info(f"Building chatbot with tools graph: {self.tool_names}")
        
        try:
            # Get tools
            tools = get_available_tools(self.tool_names)
            tool_node = create_tool_node(tools)
            
            # Bind tools to LLM
            llm_with_tools = self.llm.get_client().bind_tools(tools)
            
            def chatbot_with_tools(state: ChatbotState):
                """Chatbot node with tool calling."""
                messages = state["messages"]
                response = llm_with_tools.invoke(messages)
                return {"messages": [response]}
            
            # Build graph
            self.graph.add_node("chatbot", chatbot_with_tools)
            self.graph.add_node("tools", tool_node)
            
            self.graph.add_edge(START, "chatbot")
            self.graph.add_conditional_edges("chatbot", tools_condition)
            self.graph.add_edge("tools", "chatbot")
            
            return self.graph.compile()
        except Exception as e:
            app_logger.error(f"Failed to build chatbot with tools graph: {str(e)}")
            raise GraphException(f"Failed to build chatbot with tools graph: {str(e)}")


class ResearchGraphBuilder:
    """Builder for research agent graph."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.graph = StateGraph(ResearchState)
    
    def build(self) -> StateGraph:
        """
        Build research graph.
        
        Returns:
            Compiled graph
        """
        app_logger.info("Building research graph")
        
        try:
            search_tool = get_web_search_tool(max_results=5)
            research_node = ResearchNode(self.llm, search_tool)
            
            self.graph.add_node("search", research_node.search)
            self.graph.add_node("summarize", research_node.summarize)
            
            self.graph.add_edge(START, "search")
            self.graph.add_edge("search", "summarize")
            self.graph.add_edge("summarize", END)
            
            return self.graph.compile()
        except Exception as e:
            app_logger.error(f"Failed to build research graph: {str(e)}")
            raise GraphException(f"Failed to build research graph: {str(e)}")


class WriterGraphBuilder:
    """Builder for content writer graph."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.graph = StateGraph(WriterState)
    
    def build(self) -> StateGraph:
        """
        Build writer graph.
        
        Returns:
            Compiled graph
        """
        app_logger.info("Building writer graph")
        
        try:
            writer_node = WriterNode(self.llm)
            
            self.graph.add_node("outline", writer_node.create_outline)
            self.graph.add_node("draft", writer_node.write_draft)
            self.graph.add_node("polish", writer_node.polish)
            
            self.graph.add_edge(START, "outline")
            self.graph.add_edge("outline", "draft")
            self.graph.add_edge("draft", "polish")
            self.graph.add_edge("polish", END)
            
            return self.graph.compile()
        except Exception as e:
            app_logger.error(f"Failed to build writer graph: {str(e)}")
            raise GraphException(f"Failed to build writer graph: {str(e)}")


class GraphFactory:
    """Factory for creating different graph types."""
    
    _builders = {
        "chatbot": ChatbotGraphBuilder,
        "chatbot_with_tools": ChatbotWithToolsGraphBuilder,
        "research": ResearchGraphBuilder,
        "writer": WriterGraphBuilder
    }
    
    @classmethod
    def create(cls, graph_type: str, llm: BaseLLM, **kwargs) -> StateGraph:
        """
        Create graph based on type.
        
        Args:
            graph_type: Type of graph to create
            llm: LLM instance
            **kwargs: Additional arguments for builder
            
        Returns:
            Compiled graph
        """
        if graph_type not in cls._builders:
            raise GraphException(
                f"Unknown graph type: {graph_type}. Available: {list(cls._builders.keys())}"
            )
        
        builder_class = cls._builders[graph_type]
        builder = builder_class(llm, **kwargs)
        return builder.build()
    
    @classmethod
    def register_builder(cls, name: str, builder_class: type):
        """Register a new graph builder."""
        cls._builders[name] = builder_class
        app_logger.info(f"Registered graph builder: {name}")
