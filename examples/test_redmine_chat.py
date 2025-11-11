"""
Test script for Redmine chatbot.

Usage:
    python examples/test_redmine_chat.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.graphs.redmine import RedmineChatbotGraph
from src.llms.base import LLMFactory


async def main():
    """Test Redmine chatbot."""
    
    print("=" * 70)
    print("Redmine Chatbot Test")
    print("Chat with your Redmine platform using natural language")
    print("=" * 70)
    
    # Initialize LLM
    print("\n1️⃣  Initializing LLM...")
    try:
        llm = LLMFactory.create("groq")
        print("✅ LLM initialized")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        return
    
    # Create chatbot
    print("\n2️⃣  Creating Redmine chatbot...")
    try:
        chatbot = RedmineChatbotGraph(llm)
        print("✅ Chatbot created with 8 Redmine tools")
    except Exception as e:
        print(f"❌ Failed to create chatbot: {e}")
        return
    
    # Interactive chat loop
    print("\n3️⃣  Starting chat session...")
    print("="* 70)
    print("\n💡 Example queries:")
    print("  - Show me all my projects")
    print("  - What are the open issues?")
    print("  - Show me issue #123")
    print("  - Create a new bug: Fix login error")
    print("  - Search for issues about payment")
    print("\nType 'quit' or 'exit' to end the session\n")
    
    conversation_id = "test_session_001"
    state = None
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            # Process message
            print("\nAssistant: ", end="", flush=True)
            result = await chatbot.achat(
                message=user_input,
                conversation_id=conversation_id,
                state=state
            )
            
            # Update state for context
            state = result
            
            # Get response
            last_message = result["messages"][-1]
            response = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat session ended")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
