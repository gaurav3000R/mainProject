#!/usr/bin/env python3
"""
Quick LangSmith tracing verification.
Tests a single graph to confirm tracing is working.
"""

import os
from langchain_core.messages import HumanMessage

# Import deployable FIRST - this sets up LangSmith tracing
from src.agents.graphs.deployable import chatbot_graph
from src.utils.langsmith import verify_langsmith_connection, get_langsmith_url


def main():
    """Quick verification test."""
    print("="*70)
    print("🔍 LANGSMITH QUICK VERIFICATION")
    print("="*70)
    
    # Check config AFTER deployable import
    print(f"\n📋 Configuration (after import):")
    print(f"   Tracing Enabled: {os.getenv('LANGCHAIN_TRACING_V2')}")
    print(f"   Project: {os.getenv('LANGCHAIN_PROJECT')}")
    print(f"   API Key: {'SET' if os.getenv('LANGCHAIN_API_KEY') else 'NOT SET'}")
    print(f"   Dashboard: {get_langsmith_url()}")
    
    # Check if tracing is enabled
    if os.getenv('LANGCHAIN_TRACING_V2') not in ('true', 'True', '1'):
        print("\n❌ ERROR: LANGCHAIN_TRACING_V2 is not set to 'true'")
        print("\nCheck your .env file:")
        print("  LANGCHAIN_TRACING_V2=true")
        print("  LANGCHAIN_API_KEY=your_key_here")
        print("  LANGCHAIN_PROJECT=agentic-ai-platform")
        return False
    
    # Verify connection
    print(f"\n📡 Testing connection...")
    if not verify_langsmith_connection():
        print("\n❌ Connection failed!")
        return False
    
    # Test a graph
    print(f"\n🧪 Testing chatbot graph with tracing...")
    graph = chatbot_graph()
    
    state = {"messages": [HumanMessage(content="Test message for LangSmith")]}
    result = graph.invoke(state)
    
    print(f"\n✅ SUCCESS! Trace should be visible in LangSmith")
    print(f"\n🔗 View your traces at:")
    print(f"   {get_langsmith_url()}")
    print(f"\nLook for:")
    print(f"  • Recent trace (just now)")
    print(f"  • Run name: 'CompiledStateGraph' or similar")
    print(f"  • Project: {os.getenv('LANGCHAIN_PROJECT')}")
    print(f"  • Should show the full execution trace")
    print(f"  • Including LLM calls and node executions")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
