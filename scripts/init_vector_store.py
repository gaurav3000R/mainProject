#!/usr/bin/env python3
"""
Initialize and populate Redmine vector store for semantic search.

This script loads issue descriptions from redmine_metadata.json
and indexes them in ChromaDB for semantic similarity search.
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.redmine_vectorstore import redmine_vectorstore
from src.utils.logger import app_logger


async def main():
    """Initialize vector store."""
    print("="*70)
    print("REDMINE VECTOR STORE INITIALIZATION")
    print("="*70)
    
    if not redmine_vectorstore.is_available():
        print("\n❌ Vector store not available!")
        print("\nInstall required packages:")
        print("  pip install chromadb langchain-chroma sentence-transformers")
        return
    
    print("\n✅ Vector store service available")
    
    # Load current stats
    stats = redmine_vectorstore.get_stats()
    print(f"\n📊 Current Status:")
    print(f"   Collection: {stats.get('collection_name', 'N/A')}")
    print(f"   Documents: {stats.get('document_count', 0)}")
    print(f"   Location: {stats.get('persist_directory', 'N/A')}")
    
    # Ask user if they want to refresh
    print("\n🔄 Loading data from redmine_metadata.json...")
    
    try:
        # Load issues
        print("\n1️⃣  Loading issues...")
        redmine_vectorstore.load_from_metadata()
        
        # Load projects
        print("\n2️⃣  Loading project descriptions...")
        redmine_vectorstore.load_projects_from_metadata()
        
        # Get final stats
        final_stats = redmine_vectorstore.get_stats()
        
        print("\n" + "="*70)
        print("✅ VECTOR STORE INITIALIZED SUCCESSFULLY!")
        print("="*70)
        
        print(f"\n📦 Final Statistics:")
        print(f"   Total Documents: {final_stats.get('document_count', 0)}")
        print(f"   Collection: {final_stats.get('collection_name', 'N/A')}")
        print(f"   Storage: {final_stats.get('persist_directory', 'N/A')}")
        
        print("\n🎯 Capabilities Enabled:")
        print("   ✅ Semantic issue search")
        print("   ✅ Find similar issues")
        print("   ✅ Content-based discovery")
        print("   ✅ Project-scoped semantic search")
        
        print("\n💡 Usage in Chatbot:")
        print('   • "Find issues similar to authentication problems"')
        print('   • "Show issues related to database performance"')
        print('   • "What issues mention payment gateway?"')
        
        print("\n🚀 Vector store is ready for semantic search!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    asyncio.run(main())
