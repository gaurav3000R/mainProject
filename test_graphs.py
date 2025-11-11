#!/usr/bin/env python3
"""
Test script to check each LangGraph workflow one by one.
Usage: python test_graphs.py [graph_name]
"""

import sys
from langchain_core.messages import HumanMessage
from src.agents.graphs.deployable import (
    chatbot_graph,
    chatbot_with_tools_graph,
    research_graph,
    writer_graph,
    news_graph,
    redmine_graph
)


def test_chatbot():
    """Test simple chatbot graph."""
    print("\n" + "="*60)
    print("Testing: CHATBOT")
    print("="*60)
    
    graph = chatbot_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test invocation
    state = {"messages": [HumanMessage(content="Hello! Tell me a joke.")]}
    result = graph.invoke(state)
    
    print(f"\n📤 Input: Hello! Tell me a joke.")
    print(f"📥 Output: {result['messages'][-1].content[:200]}...")
    print("✅ CHATBOT WORKING")


def test_chatbot_with_tools():
    """Test chatbot with tools graph."""
    print("\n" + "="*60)
    print("Testing: CHATBOT WITH TOOLS")
    print("="*60)
    
    graph = chatbot_with_tools_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test invocation (simple query to avoid tool calling)
    state = {"messages": [HumanMessage(content="What is 2+2?")]}
    result = graph.invoke(state)
    
    print(f"\n📤 Input: What is 2+2?")
    print(f"📥 Output: {result['messages'][-1].content[:200]}...")
    print("✅ CHATBOT WITH TOOLS WORKING")


def test_research():
    """Test research agent graph."""
    print("\n" + "="*60)
    print("Testing: RESEARCH AGENT")
    print("="*60)
    
    graph = research_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test with a simple query (won't actually search in demo)
    state = {
        "query": "Python programming",
        "search_results": [],
        "sources": [],
        "summary": ""
    }
    
    print(f"\n📤 Input: Query='Python programming'")
    print(f"  Note: This will attempt web search. May take a moment...")
    
    try:
        result = graph.invoke(state)
        print(f"📥 Found {len(result.get('search_results', []))} results")
        print(f"📝 Summary: {result.get('summary', '')[:200]}...")
        print("✅ RESEARCH AGENT WORKING")
    except Exception as e:
        print(f"⚠️  Research agent error (may need API keys): {str(e)[:100]}")


def test_writer():
    """Test content writer graph."""
    print("\n" + "="*60)
    print("Testing: CONTENT WRITER")
    print("="*60)
    
    graph = writer_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test invocation
    state = {
        "topic": "Benefits of exercise",
        "content_type": "blog post",
        "outline": "",
        "draft": "",
        "final_content": ""
    }
    
    print(f"\n📤 Input: Topic='Benefits of exercise'")
    print(f"  Note: This will generate outline → draft → polish. May take 30-60 seconds...")
    
    try:
        result = graph.invoke(state)
        print(f"\n📝 Outline: {result.get('outline', '')[:150]}...")
        print(f"📝 Draft: {result.get('draft', '')[:150]}...")
        print(f"📝 Final: {result.get('final_content', '')[:150]}...")
        print("✅ CONTENT WRITER WORKING")
    except Exception as e:
        print(f"⚠️  Writer error: {str(e)[:100]}")


def test_news():
    """Test news summarization graph."""
    print("\n" + "="*60)
    print("Testing: NEWS SUMMARIZATION")
    print("="*60)
    
    graph = news_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test invocation
    state = {
        "query": "AI technology",
        "max_results": 3,
        "news_articles": [],
        "summary": "",
        "saved_path": None,
        "error": None,
        "status": "started"
    }
    
    print(f"\n📤 Input: Query='AI technology', max_results=3")
    print(f"  Note: This will fetch news and summarize. May take a moment...")
    
    try:
        result = graph.invoke(state)
        print(f"📥 Status: {result.get('status')}")
        print(f"📰 Articles found: {len(result.get('news_articles', []))}")
        print(f"📝 Summary: {result.get('summary', '')[:200]}...")
        if result.get('saved_path'):
            print(f"💾 Saved to: {result.get('saved_path')}")
        print("✅ NEWS SUMMARIZATION WORKING")
    except Exception as e:
        print(f"⚠️  News error (may need API keys): {str(e)[:100]}")


def test_redmine():
    """Test Redmine chatbot graph."""
    print("\n" + "="*60)
    print("Testing: REDMINE CHATBOT")
    print("="*60)
    
    graph = redmine_graph()
    print(f"✓ Graph compiled successfully")
    print(f"  Nodes: {[n for n in graph.nodes.keys() if n != '__start__']}")
    
    # Test invocation
    state = {
        "messages": [HumanMessage(content="List all projects")],
        "conversation_id": "test-123",
        "current_project_id": None,
        "current_issue_id": None
    }
    
    print(f"\n📤 Input: List all projects")
    print(f"  Note: This will use Redmine tools. May need API access...")
    
    try:
        result = graph.invoke(state)
        print(f"📥 Output: {result['messages'][-1].content[:200]}...")
        print("✅ REDMINE CHATBOT WORKING")
    except Exception as e:
        print(f"⚠️  Redmine error (may need API setup): {str(e)[:100]}")


# Available tests
TESTS = {
    "chatbot": test_chatbot,
    "chatbot_with_tools": test_chatbot_with_tools,
    "research": test_research,
    "writer": test_writer,
    "news": test_news,
    "redmine": test_redmine,
    "all": None  # Special case
}


def main():
    """Main test runner."""
    print("="*60)
    print("🧪 LANGGRAPH WORKFLOW TESTER")
    print("="*60)
    
    # Parse arguments
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
    else:
        print("\nAvailable tests:")
        for i, name in enumerate(TESTS.keys(), 1):
            print(f"  {i}. {name}")
        print("\nUsage: python test_graphs.py <test_name>")
        print("Example: python test_graphs.py chatbot")
        print("         python test_graphs.py all")
        return
    
    # Run test(s)
    if test_name == "all":
        for name, test_fn in TESTS.items():
            if name != "all":
                try:
                    test_fn()
                except Exception as e:
                    print(f"\n❌ {name.upper()} FAILED: {str(e)}")
                print()
    elif test_name in TESTS:
        try:
            TESTS[test_name]()
        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Unknown test: {test_name}")
        print(f"Available: {', '.join(TESTS.keys())}")


if __name__ == "__main__":
    main()
