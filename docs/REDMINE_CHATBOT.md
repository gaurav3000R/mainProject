# Redmine Chatbot - Complete Guide

## 🎯 Overview

A natural language chatbot powered by LangGraph and LangChain that allows you to interact with your Redmine project management platform through conversation.

**Workflow:** User Query → LLM decides action → Calls Redmine Tools → Returns formatted response

## 🚀 Quick Start

### 1. Configuration

Ensure your `.env` file has:
```bash
REDMIN_API_BASE_URL=https://your-redmine.com/
REDMIN_API_KEY=your_api_key_here
```

### 2. Start Server
```bash
python main.py
```

### 3. Validate Connection
```bash
curl http://localhost:8000/api/v1/redmine/validate
```

### 4. Start Chatting
```bash
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me all my projects"
  }'
```

## 📡 API Endpoints

### 1. Chat with Redmine
```
POST /api/v1/redmine/chat
```

**Request:**
```json
{
  "message": "Show me all open issues",
  "conversation_id": "optional-for-context"
}
```

**Response:**
```json
{
  "message": "Found 10 open issues:\n- #123: Fix login bug...",
  "conversation_id": "abc123",
  "tool_calls": ["get_redmine_issues"],
  "metadata": {
    "message_count": 4,
    "tools_used": true
  }
}
```

### 2. Validate Connection
```
POST /api/v1/redmine/validate
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully connected to Redmine",
  "user_info": {
    "id": 1,
    "login": "admin",
    "firstname": "John",
    "lastname": "Doe"
  }
}
```

### 3. Get Capabilities
```
GET /api/v1/redmine/capabilities
```

Returns list of available commands and example queries.

### 4. Health Check
```
GET /api/v1/redmine/health
```

## 🤖 What Can the Chatbot Do?

### Project Management
- **View Projects**: "Show me all projects"
- **Project Details**: "What projects are available?"

### Issue Management
- **List Issues**: "Show me all open issues"
- **Get Details**: "Show me issue #123"
- **Create Issues**: "Create a new bug in project 5 about login error"
- **Update Issues**: "Update issue #45 to closed"
- **Search Issues**: "Find issues about authentication"

### Time Tracking
- **View Time Entries**: "Show me time entries for project 3"
- **Time Summary**: "How much time was logged this week?"

### Metadata
- **Get Statuses**: "What statuses are available?"
- **Get Priorities**: "Show me priority levels"
- **Get Trackers**: "What trackers do we have?"

## 💬 Example Conversations

### Example 1: Viewing Projects
```
User: "What projects do I have?"
Assistant: "Found 5 projects:
- Project Alpha (ID: 1)
- Project Beta (ID: 2)
- ..."
```

### Example 2: Creating an Issue
```
User: "Create a new bug in project 5: User cannot login"
Assistant: "✅ Successfully created issue #456: User cannot login"

User: "Add more details to issue #456"
Assistant: "I can help update issue #456. What details would you like to add?"
```

### Example 3: Searching Issues
```
User: "Find all issues about payment processing"
Assistant: "Found 3 issues matching 'payment processing':
- #234: Payment gateway timeout
- #245: Failed payment notifications
- #289: Payment history not showing"
```

### Example 4: Multi-turn Conversation
```
User: "Show me open issues for project 3"
Assistant: "Found 8 open issues in Project Alpha..."

User: "What about the critical ones?"
Assistant: [Uses context to filter for critical priority]
```

## 🛠️ Available Tools

The chatbot uses 8 LangChain tools to interact with Redmine:

| Tool | Description |
|------|-------------|
| `get_redmine_projects` | List all projects |
| `get_redmine_issues` | List issues with filters |
| `get_redmine_issue_details` | Get specific issue details |
| `create_redmine_issue` | Create new issue |
| `update_redmine_issue` | Update existing issue |
| `search_redmine_issues` | Search issues by keyword |
| `get_redmine_time_entries` | View time logs |
| `get_redmine_metadata` | Get statuses, priorities, trackers |

## 🏗️ Architecture

```
User Message
     ↓
LangGraph Chatbot Node
     ↓
LLM decides: Need tools? ───→ Yes → Execute Tools → Back to LLM
     ↓ No
Generate Response
     ↓
Return to User
```

### Components

1. **Redmine API Client** (`src/services/redmine_client.py`)
   - HTTP client for Redmine REST API
   - Authentication with API key
   - All CRUD operations

2. **LangChain Tools** (`src/tools/redmine.py`)
   - 8 tools decorated with `@tool`
   - Natural language descriptions
   - Async implementation

3. **LangGraph Workflow** (`src/agents/graphs/redmine.py`)
   - StateGraph with chatbot and tools nodes
   - Conditional routing based on tool needs
   - Memory integration

4. **FastAPI Endpoints** (`src/api/v1/redmine.py`)
   - REST API for chat interface
   - Conversation history management
   - Error handling

## 📊 State Management

```python
{
  "messages": [...],          # Conversation history
  "conversation_id": "...",   # Session identifier
  "current_project_id": 5,    # Context tracking
  "current_issue_id": 123     # Context tracking
}
```

## 🔧 Configuration

### Environment Variables
```bash
REDMIN_API_BASE_URL=https://your-redmine.com/
REDMIN_API_KEY=your_api_key_here
```

### Customization

#### Add Custom Tools
```python
# In src/tools/redmine.py

@tool
async def your_custom_tool(param: str) -> str:
    """Description for LLM."""
    # Your logic here
    return result

# Add to redmine_tools list
```

#### Modify System Prompt
```python
# In src/agents/graphs/redmine.py

def _create_system_message(self):
    return SystemMessage(content="Your custom instructions...")
```

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:8000/api/v1/redmine/health

# Validate connection
curl -X POST http://localhost:8000/api/v1/redmine/validate

# Chat
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all projects"}'
```

### Python Testing
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/redmine/chat",
    json={"message": "What are my open issues?"}
)
print(response.json()["message"])
```

## 📚 Integration Examples

### Standalone Usage
```python
from src.agents.graphs.redmine import RedmineChatbotGraph
from src.llms.base import LLMFactory

llm = LLMFactory.create("groq")
chatbot = RedmineChatbotGraph(llm)

result = await chatbot.achat(
    message="Show me project 5 issues",
    conversation_id="session_123"
)
print(result["messages"][-1].content)
```

### With Memory
```python
from src.services.memory import memory_manager

# Conversation persists
response1 = await chatbot.achat("Show me project 5", "conv_1")
response2 = await chatbot.achat("What about its issues?", "conv_1")
# Context is maintained across turns
```

## 🎯 Use Cases

1. **Daily Standup**: "Show me all issues assigned to me"
2. **Project Planning**: "List all projects and their open issues"
3. **Quick Issue Creation**: "Create a bug: Homepage not loading"
4. **Status Updates**: "Update issue #123 to in progress"
5. **Time Tracking**: "Show me this week's time entries"
6. **Search & Analysis**: "Find all critical bugs in project 7"

## 🔒 Security

- API keys stored in `.env` (not committed)
- HTTPS recommended for production
- Rate limiting available via middleware
- Input validation on all endpoints

## 🐛 Troubleshooting

### Issue: "Redmine API not configured"
**Solution**: Check `.env` file has correct `REDMIN_API_BASE_URL` and `REDMIN_API_KEY`

### Issue: Connection timeout
**Solution**: Verify Redmine URL is accessible and API key is valid

### Issue: Tool not being called
**Solution**: Make tool descriptions more explicit for LLM to understand when to use them

### Issue: Context not maintained
**Solution**: Always pass the same `conversation_id` in subsequent requests

## 📈 Performance

- **Average response time**: 2-5 seconds
- **Concurrent requests**: Supported via async
- **Memory**: Stores last 20 messages per conversation
- **Rate limits**: Configurable per Redmine instance

## 🚀 Future Enhancements

- [ ] Bulk operations (create multiple issues)
- [ ] Advanced filtering (date ranges, custom fields)
- [ ] Issue attachments support
- [ ] Gantt chart generation
- [ ] Email notifications
- [ ] Webhook integration
- [ ] Multi-language support
- [ ] Voice interface

## 📖 Related Documentation

- [Redmine REST API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Conversation Memory](./CONVERSATION_MEMORY.md)

## ✅ Files Created

```
src/
├── services/
│   └── redmine_client.py      # Redmine API client
├── tools/
│   └── redmine.py              # LangChain tools
├── agents/
│   ├── states/
│   │   └── redmine.py          # State definition
│   └── graphs/
│       └── redmine.py          # LangGraph workflow
└── api/
    └── v1/
        └── redmine.py          # FastAPI endpoints

redminDocs/
├── api_details.json            # API reference
└── Redmine API Information...  # Additional docs
```

## 🎉 Ready to Use!

Your Redmine chatbot is fully configured and ready to help manage your projects through natural language!

Start chatting: `POST /api/v1/redmine/chat`
