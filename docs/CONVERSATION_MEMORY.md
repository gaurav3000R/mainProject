# Conversation Memory System

## Overview

The chatbot now includes a conversation memory system that remembers and uses past conversations, making your AI agent context-aware and more intelligent.

## Features

### 1. **Conversation History**
- Automatically stores all user and AI messages
- Each conversation has a unique ID
- Maintains conversation context across multiple requests

### 2. **Context-Aware Responses**
- AI can reference previous messages
- Follow-up questions work naturally
- Maintains conversation flow

### 3. **Memory Management**
- Automatic trimming to prevent memory overflow (default: 20 messages)
- Per-conversation metadata tracking
- List, view, and delete conversations

## API Endpoints

### Chat with Memory
```bash
POST /api/v1/chat/
{
  "message": "Hello, what's the weather?",
  "conversation_id": "abc123"  # optional, generated if not provided
}
```

**Response:**
```json
{
  "message": "I'll help you check the weather...",
  "conversation_id": "abc123",
  "metadata": {
    "message_count": 2,
    "history_length": 0,
    "has_tool_calls": true
  }
}
```

### List All Conversations
```bash
GET /api/v1/chat/conversations
```

**Response:**
```json
{
  "conversations": [
    {
      "conversation_id": "abc123",
      "created_at": "2025-11-10T23:20:00",
      "message_count": 6,
      "last_activity": "2025-11-10T23:25:00"
    }
  ],
  "total": 1
}
```

### Get Conversation History
```bash
GET /api/v1/chat/conversations/{conversation_id}
```

**Response:**
```json
{
  "conversation_id": "abc123",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?"
    }
  ],
  "metadata": {
    "created_at": "2025-11-10T23:20:00",
    "message_count": 2
  }
}
```

### Clear Conversation
```bash
POST /api/v1/chat/conversations/{conversation_id}/clear
```

### Delete Conversation
```bash
DELETE /api/v1/chat/conversations/{conversation_id}
```

## Usage Examples

### Example 1: Multi-Turn Conversation
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# First message
response1 = requests.post(f"{BASE_URL}/chat/", json={
    "message": "My name is Alice"
})
conv_id = response1.json()["conversation_id"]

# Follow-up (AI remembers the name)
response2 = requests.post(f"{BASE_URL}/chat/", json={
    "message": "What's my name?",
    "conversation_id": conv_id
})
print(response2.json()["message"])  # Output: "Your name is Alice"
```

### Example 2: Context Awareness
```bash
# First request
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a meeting at 3pm"}'

# Save the conversation_id from response

# Follow-up request
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What time is my meeting?",
    "conversation_id": "YOUR_CONVERSATION_ID"
  }'
```

### Example 3: View Conversation History
```bash
curl http://localhost:8000/api/v1/chat/conversations/YOUR_CONVERSATION_ID
```

## Configuration

Adjust memory settings in `src/services/memory.py`:

```python
# Change max messages per conversation
memory_manager = ConversationMemoryManager(
    max_messages_per_conversation=50  # Default is 20
)
```

## Architecture

### Components

1. **ConversationMemoryManager** (`src/services/memory.py`)
   - Core memory management
   - In-memory storage (can be extended to Redis/PostgreSQL)
   - Automatic history trimming

2. **Chat Endpoints** (`src/api/v1/chat.py`)
   - Integrated with memory manager
   - Stores user and AI messages automatically
   - Retrieves history for context

### Flow

```
User Request
    ↓
Generate/Use conversation_id
    ↓
Retrieve conversation history
    ↓
Combine history + new message
    ↓
Send to LLM with full context
    ↓
Store AI response
    ↓
Return response with conversation_id
```

## Advanced Features

### Extending to Persistent Storage

The current implementation uses in-memory storage. To add persistent storage:

```python
# src/services/memory.py

class RedisChatMessageHistory(BaseChatMessageHistory):
    """Redis-backed chat history"""
    
    def __init__(self, conversation_id: str, redis_url: str):
        import redis
        self.redis_client = redis.from_url(redis_url)
        self.conversation_id = conversation_id
    
    def add_message(self, message: BaseMessage):
        # Store in Redis
        pass
    
    @property
    def messages(self) -> List[BaseMessage]:
        # Retrieve from Redis
        pass
```

### Adding Vector-Based Semantic Memory

For semantic search over conversation history:

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class SemanticMemory:
    """Vector-based semantic memory"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstores = {}
    
    def add_to_memory(self, conversation_id: str, text: str):
        if conversation_id not in self.vectorstores:
            self.vectorstores[conversation_id] = FAISS.from_texts(
                [text], self.embeddings
            )
        else:
            self.vectorstores[conversation_id].add_texts([text])
    
    def search_memory(self, conversation_id: str, query: str, k: int = 3):
        if conversation_id in self.vectorstores:
            return self.vectorstores[conversation_id].similarity_search(query, k=k)
        return []
```

## Best Practices

1. **Use Conversation IDs**: Always pass the conversation_id for follow-up messages
2. **Monitor Memory Usage**: Check conversation counts regularly
3. **Cleanup Old Conversations**: Delete inactive conversations periodically
4. **Adjust History Length**: Tune `max_messages_per_conversation` based on your use case
5. **Handle Context Window**: Consider token limits when including history

## Troubleshooting

### Q: AI doesn't remember previous messages
**A:** Make sure you're passing the same `conversation_id` in follow-up requests.

### Q: Conversations growing too large
**A:** Reduce `max_messages_per_conversation` or implement custom trimming logic.

### Q: Need persistent storage
**A:** Implement a custom `BaseChatMessageHistory` with Redis/PostgreSQL backend.

## Future Enhancements

- [ ] Vector-based semantic memory
- [ ] Persistent storage (Redis/PostgreSQL)
- [ ] Conversation summarization
- [ ] Memory compression
- [ ] Multi-user support with user IDs
- [ ] Conversation export/import
- [ ] Analytics and insights

## Related Files

- `src/services/memory.py` - Core memory implementation
- `src/api/v1/chat.py` - Chat endpoints with memory integration
- `src/schemas/api.py` - Request/response schemas
