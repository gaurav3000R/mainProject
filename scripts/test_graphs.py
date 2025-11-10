#!/usr/bin/env python3
"""
Quick test script to run all graphs individually.
This demonstrates Method 3: Python Direct Import
"""
from langchain_core.messages import HumanMessage
from src.agents.graphs.deployable import (
    chatbot_graph,
    chatbot_with_tools_graph,
    research_graph,
    writer_graph
)

def test_chatbot():
    """Test simple chatbot graph."""
    print("\n" + "="*60)
    print("🤖 Testing: CHATBOT")
    print("="*60)
    
    graph = chatbot_graph()
    result = graph.invoke({
        "messages": [HumanMessage(content="Hello! Tell me a fun fact about AI.")]
    })
    
    print(f"Response: {result['messages'][-1].content}")
    print("✅ Chatbot test passed!")


def test_chatbot_with_tools():
    """Test chatbot with tools graph."""
    print("\n" + "="*60)
    print("🔧 Testing: CHATBOT WITH TOOLS")
    print("="*60)
    
    graph = chatbot_with_tools_graph()
    result = graph.invoke({
        "messages": [HumanMessage(content="Hi! Just say hello back.")]
    })
    
    print(f"Response: {result['messages'][-1].content}")
    print("✅ Chatbot with tools test passed!")


def test_research_agent():
    """Test research agent graph."""
    print("\n" + "="*60)
    print("🔬 Testing: RESEARCH AGENT")
    print("="*60)
    
    graph = research_graph()
    result = graph.invoke({
        "query": "What is LangGraph?",
        "max_results": 2
    })
    
    print(f"Summary: {result.get('summary', 'No summary')[:200]}...")
    print(f"Sources found: {len(result.get('sources', []))}")
    print("✅ Research agent test passed!")


def test_content_writer():
    """Test content writer graph."""
    print("\n" + "="*60)
    print("✍️  Testing: CONTENT WRITER")
    print("="*60)
    
    graph = writer_graph()
    result = graph.invoke({
        "topic": "Benefits of AI Agents",
        "content_type": "blog",
        "tone": "professional"
    })
    
    print(f"Outline: {result.get('outline', 'No outline')[:150]}...")
    print(f"Draft length: {len(result.get('draft', ''))} chars")
    print(f"Final length: {len(result.get('final_content', ''))} chars")
    print("✅ Content writer test passed!")


def main():
    """Run all graph tests."""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚀 TESTING ALL GRAPHS - PYTHON DIRECT IMPORT".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        test_chatbot()
        test_chatbot_with_tools()
        test_research_agent()
        test_content_writer()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nAll 4 graphs are working correctly!")
        print("View traces at: https://smith.langchain.com")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
