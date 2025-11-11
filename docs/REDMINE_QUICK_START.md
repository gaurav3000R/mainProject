# Redmine Chatbot - Quick Reference

## 🎯 What You Got

A complete conversational AI chatbot for your Redmine platform with:
- **8 LangChain Tools** for Redmine operations
- **LangGraph Workflow** for intelligent routing
- **FastAPI Endpoints** for REST API access
- **Conversation Memory** for context-aware chat

## 🚀 Quick Test

### 1. Validate Connection
```bash
curl -X POST http://localhost:8000/api/v1/redmine/validate
```

### 2. Start Chatting
```bash
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me all my projects"
  }'
```

### 3. Interactive Test
```bash
python examples/test_redmine_chat.py
```

## 💬 Example Queries

### Projects
```
"Show me all projects"
"What projects do I have access to?"
"List all available projects"
```

### Issues
```
"Show me all open issues"
"What issues are assigned to me?"
"Show me details of issue #123"
"Find all critical bugs"
```

### Create & Update
```
"Create a new bug in project 5: User can't login"
"Update issue #45 status to closed"
"Create a feature request: Add dark mode"
```

### Search
```
"Search for issues about authentication"
"Find all payment related issues"
"Show me bugs containing 'timeout'"
```

### Time & Metadata
```
"Show me time entries for project 3"
"What statuses are available?"
"List all priority levels"
```

## 🛠️ Available Tools

| Tool | What It Does |
|------|--------------|
| **get_redmine_projects** | Lists all projects |
| **get_redmine_issues** | Lists issues with filters |
| **get_redmine_issue_details** | Gets specific issue info |
| **create_redmine_issue** | Creates new issue |
| **update_redmine_issue** | Updates existing issue |
| **search_redmine_issues** | Searches by keywords |
| **get_redmine_time_entries** | Shows time logs |
| **get_redmine_metadata** | Gets statuses/priorities |

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/redmine/chat` | POST | Chat with Redmine |
| `/api/v1/redmine/validate` | POST | Test connection |
| `/api/v1/redmine/capabilities` | GET | List features |
| `/api/v1/redmine/health` | GET | Health check |

## 📝 Request Format

```json
{
  "message": "Your natural language query",
  "conversation_id": "optional-session-id"
}
```

## 📤 Response Format

```json
{
  "message": "AI assistant response",
  "conversation_id": "session-id",
  "tool_calls": ["get_redmine_projects"],
  "metadata": {
    "message_count": 4,
    "tools_used": true
  }
}
```

## 🔧 Configuration

Required in `.env`:
```bash
REDMIN_API_BASE_URL=https://your-redmine.com/
REDMIN_API_KEY=your_api_key_here
```

## 🏗️ Architecture

```
User Query
    ↓
LangGraph Chatbot
    ↓
Decides: Need tools?
    ↓ Yes
Execute Redmine Tools
    ↓
Format Response
    ↓
Return to User
```

## 📂 Files Created

```
src/
├── services/redmine_client.py    # HTTP client
├── tools/redmine.py               # 8 LangChain tools
├── agents/
│   ├── states/redmine.py         # State definition
│   └── graphs/redmine.py         # LangGraph workflow
└── api/v1/redmine.py             # FastAPI endpoints

examples/
└── test_redmine_chat.py          # Interactive test

docs/
└── REDMINE_CHATBOT.md            # Full documentation
```

## 🎯 Key Features

✅ Natural language interface  
✅ Context-aware conversations  
✅ Automatic tool selection  
✅ Project & issue management  
✅ Search & filtering  
✅ Time tracking  
✅ Create & update operations  
✅ Metadata access  

## 🐛 Troubleshooting

**Can't connect**: Check `.env` has correct URL and API key  
**Slow responses**: Normal for first request (tool loading)  
**Tool not called**: Make query more specific  
**Lost context**: Use same `conversation_id` in requests  

## 📚 Next Steps

1. **Test connection**: `/api/v1/redmine/validate`
2. **Try examples**: See "Example Queries" above
3. **Read full docs**: `docs/REDMINE_CHATBOT.md`
4. **Integrate**: Use in your app via REST API

## 🎉 You're All Set!

Start chatting with your Redmine platform now!

```bash
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all open issues"}'
```
