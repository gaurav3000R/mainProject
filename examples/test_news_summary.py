"""
Test script for news summarization workflow.

Usage:
    python examples/test_news_summary.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.graphs.news import NewsSummarizationGraph
from src.llms.base import LLMFactory


async def main():
    """Test news summarization workflow."""
    
    print("=" * 70)
    print("News Summarization Workflow Test")
    print("Workflow: Start → Fetch News → Summarize → Save → End")
    print("=" * 70)
    
    # Initialize LLM
    print("\n1️⃣  Initializing LLM...")
    try:
        llm = LLMFactory.create("groq")
        print("✅ LLM initialized")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        return
    
    # Create workflow graph
    print("\n2️⃣  Creating workflow graph...")
    graph = NewsSummarizationGraph(llm)
    print("✅ Graph created")
    
    # Get query from user
    print("\n3️⃣  Enter search query:")
    query = input("   Query (e.g., 'AI news today'): ").strip()
    if not query:
        query = "artificial intelligence news"
        print(f"   Using default: {query}")
    
    max_results = input("   Max results (default 5): ").strip()
    max_results = int(max_results) if max_results else 5
    
    # Run workflow
    print(f"\n4️⃣  Running workflow for: {query}")
    print("   This may take 10-30 seconds...")
    print()
    
    try:
        result = await graph.arun(query=query, max_results=max_results)
        
        # Display results
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        
        print(f"\n📊 Status: {result['status']}")
        print(f"📰 Articles Fetched: {len(result.get('news_articles', []))}")
        
        if result.get('error'):
            print(f"\n❌ Error: {result['error']}")
        else:
            print(f"\n📝 Summary:")
            print("-" * 70)
            print(result.get('summary', 'No summary generated'))
            print("-" * 70)
            
            if result.get('saved_path'):
                print(f"\n💾 Saved to: {result['saved_path']}")
            
            # Show article titles
            if result.get('news_articles'):
                print(f"\n📑 Article Titles:")
                for i, article in enumerate(result['news_articles'], 1):
                    print(f"   {i}. {article.get('title', 'Untitled')}")
        
        print("\n" + "=" * 70)
        print("✅ Workflow completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
