#!/usr/bin/env python3
"""
Test LangSmith tracing with all graphs.
Run this to verify traces are being sent to LangSmith.
"""

import os
import sys
from datetime import datetime
from langchain_core.messages import HumanMessage
from src.core.config import settings, setup_langsmith
from src.utils.langsmith import verify_langsmith_connection, get_langsmith_url
from src.agents.graphs.deployable import (
    chatbot_graph,
    chatbot_with_tools_graph,
    research_graph,
    writer_graph,
    news_graph,
    redmine_graph
)


def test_langsmith_connection():
    """Verify LangSmith connection."""
    print("="*70)
    print("🔍 LANGSMITH TRACING VERIFICATION")
    print("="*70)
    
    print(f"\n📋 Configuration:")
    print(f"   LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
    print(f"   LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
    print(f"   LANGCHAIN_ENDPOINT: {os.getenv('LANGCHAIN_ENDPOINT')}")
    print(f"   API Key: {os.getenv('LANGCHAIN_API_KEY', '')[:20]}...")
    
    print(f"\n🔗 Dashboard URL: {get_langsmith_url()}")
    
    print("\n📡 Testing connection...")
    if verify_langsmith_connection():
        print("✅ Connection successful!")
        return True
    else:
        print("❌ Connection failed!")
        return False


def test_graph_tracing(graph_name: str, graph_fn, test_input: dict):
    """Test tracing for a specific graph."""
    print(f"\n{'─'*70}")
    print(f"Testing: {graph_name.upper()}")
    print(f"{'─'*70}")
    
    try:
        # Build graph
        graph = graph_fn()
        print(f"✓ Graph compiled")
        
        # Run with tracing
        print(f"✓ Running graph with test input...")
        result = graph.invoke(test_input)
        
        print(f"✓ Graph executed successfully")
        print(f"✅ {graph_name} traced!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        return False


def main():
    """Main test runner."""
    # Setup LangSmith
    setup_langsmith()
    
    # Verify connection
    if not test_langsmith_connection():
        print("\n⚠️  LangSmith connection failed. Traces may not be sent.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("\n" + "="*70)
    print("🧪 TESTING GRAPH TRACING")
    print("="*70)
    
    # Test each graph
    tests = [
        (
            "chatbot",
            chatbot_graph,
            {"messages": [HumanMessage(content="Hello! This is a LangSmith tracing test.")]}
        ),
        (
            "chatbot_with_tools",
            chatbot_with_tools_graph,
            {"messages": [HumanMessage(content="What is 2+2?")]}
        ),
        (
            "research",
            research_graph,
            {
                "query": "Python programming",
                "search_results": [],
                "sources": [],
                "summary": ""
            }
        ),
        (
            "writer",
            writer_graph,
            {
                "topic": "Benefits of AI",
                "content_type": "article",
                "outline": "",
                "draft": "",
                "final_content": ""
            }
        ),
        (
            "news",
            news_graph,
            {
                "query": "AI news",
                "max_results": 2,
                "news_articles": [],
                "summary": "",
                "saved_path": None,
                "error": None,
                "status": "started"
            }
        ),
        (
            "redmine",
            redmine_graph,
            {
                "messages": [HumanMessage(content="What projects exist?")],
                "conversation_id": "test-langsmith",
                "current_project_id": None,
                "current_issue_id": None
            }
        ),
    ]
    
    results = {}
    for name, graph_fn, test_input in tests:
        try:
            results[name] = test_graph_tracing(name, graph_fn, test_input)
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            results[name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    success_count = sum(1 for s in results.values() if s)
    total_count = len(results)
    
    print(f"\n{success_count}/{total_count} graphs traced successfully")
    
    print("\n" + "="*70)
    print("🔗 VIEW TRACES")
    print("="*70)
    print(f"\nDashboard: {get_langsmith_url()}")
    print("\nYou should see traces for each graph execution.")
    print("Each trace will show:")
    print("  - Graph structure and node execution")
    print("  - LLM calls and responses")
    print("  - Tool invocations")
    print("  - Execution times")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
