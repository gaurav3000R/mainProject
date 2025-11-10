# 🎯 How to Run a Specific Graph

There are **4 ways** to run your LangGraph graphs. Choose based on your use case:

---

## Method 1: 🎨 LangGraph Studio (Visual UI) - RECOMMENDED FOR DEVELOPMENT

### Start the Server
```bash
cd mainProject

# Option A: Use the script
./scripts/start_studio.sh

# Option B: Manual start
uv run langgraph dev --port 8123
```

### Access Studio UI
Open in browser: **http://127.0.0.1:8123**

### Run a Specific Graph
1. **Select graph** from dropdown menu:
   - `chatbot`
   - `chatbot_with_tools`
   - `research_agent`
   - `content_writer`

2. **Enter input** in the chat interface
3. **Watch execution** visually
4. **Inspect state** at each node

**Perfect for:** Debugging, testing, visual understanding

---

## Method 2: 🔌 Studio API (HTTP) - PROGRAMMATIC ACCESS

When Studio server is running, use the REST API:

### Example: Run Chatbot
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "chatbot",
    "input": {
      "messages": [
        {"role": "user", "content": "Hello, how are you?"}
      ]
    },
    "config": {
      "configurable": {
        "thread_id": "user-123"
      }
    }
  }'
```

### Example: Run Research Agent
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "research_agent",
    "input": {
      "query": "Latest AI developments",
      "max_results": 5
    },
    "config": {
      "configurable": {
        "thread_id": "research-001"
      }
    }
  }'
```

### Example: Run Content Writer
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "content_writer",
    "input": {
      "topic": "Introduction to LangGraph",
      "content_type": "blog",
      "tone": "professional"
    },
    "config": {
      "configurable": {
        "thread_id": "writer-001"
      }
    }
  }'
```

**Perfect for:** Integration testing, automation, CI/CD

---

## Method 3: 🐍 Python Direct Import - IN YOUR CODE

Run graphs directly in your Python code:

### Example 1: Run Chatbot
```python
# File: test_graphs.py
from src.agents.graphs.deployable import chatbot_graph
from langchain_core.messages import HumanMessage

# Create graph
graph = chatbot_graph()

# Run it
input_data = {
    "messages": [HumanMessage(content="Hello, tell me about LangGraph")]
}

result = graph.invoke(input_data)
print(result["messages"][-1].content)
```

Run it:
```bash
uv run python test_graphs.py
```

### Example 2: Run Research Agent
```python
from src.agents.graphs.deployable import research_graph

graph = research_graph()

result = graph.invoke({
    "query": "Impact of AI on healthcare",
    "max_results": 5
})

print("Summary:", result["summary"])
print("Sources:", result["sources"])
```

### Example 3: Run Content Writer
```python
from src.agents.graphs.deployable import writer_graph

graph = writer_graph()

result = graph.invoke({
    "topic": "Future of AI Agents",
    "content_type": "blog",
    "tone": "professional"
})

print("Outline:", result["outline"])
print("Draft:", result["draft"])
print("Final:", result["final_content"])
```

### Example 4: Run with Streaming
```python
from src.agents.graphs.deployable import chatbot_with_tools_graph
from langchain_core.messages import HumanMessage

graph = chatbot_with_tools_graph()

input_data = {
    "messages": [HumanMessage(content="What's the weather in Tokyo?")]
}

# Stream results
for chunk in graph.stream(input_data):
    print(chunk)
```

**Perfect for:** Custom scripts, testing, local development

---

## Method 4: 🌐 FastAPI Endpoints - PRODUCTION API

Use your existing FastAPI endpoints:

### Start FastAPI Server
```bash
uv run python main.py
# Or
uv run uvicorn main:app --reload --port 8000
```

### Available Endpoints

#### 1. Simple Chatbot
```bash
curl -X POST http://localhost:8000/api/v1/chat/simple \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?"
  }'
```

#### 2. Chatbot with Tools
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest AI developments in 2024?"
  }'
```

#### 3. Research Agent
```bash
curl -X POST http://localhost:8000/api/v1/research/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Impact of AI on healthcare",
    "max_results": 5
  }'
```

#### 4. Content Writer
```bash
curl -X POST http://localhost:8000/api/v1/writer/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Future of Artificial Intelligence",
    "content_type": "blog",
    "tone": "professional"
  }'
```

**Perfect for:** Production deployment, external integrations

---

## 📊 Quick Comparison

| Method | Use Case | When to Use |
|--------|----------|-------------|
| **Studio UI** | Visual debugging | Development, testing |
| **Studio API** | Programmatic access | Automation, testing |
| **Python Import** | Direct execution | Scripts, experiments |
| **FastAPI** | Production API | Deployment, apps |

---

## 🎯 Which Method Should I Use?

### For Development & Debugging:
✅ **Use Studio UI (Method 1)**
- Visual feedback
- Step-by-step execution
- State inspection
- Easy testing

### For Testing & Automation:
✅ **Use Studio API (Method 2) or Python (Method 3)**
- Programmatic control
- CI/CD integration
- Automated tests
- Quick iterations

### For Production:
✅ **Use FastAPI (Method 4)**
- RESTful API
- Authentication
- Rate limiting
- Scalable

---

## 💡 Pro Tips

### 1. Run Multiple Graphs Simultaneously
```bash
# Terminal 1: Studio (for debugging)
uv run langgraph dev --port 8123

# Terminal 2: FastAPI (for production API)
uv run python main.py
```

### 2. Use Thread IDs for Conversation Tracking
```python
# Studio API
config = {
    "configurable": {
        "thread_id": "user-123-session-abc"
    }
}
```

### 3. Stream Results for Real-time Updates
```python
# Python streaming
for event in graph.stream(input_data):
    print(event)
```

### 4. Check Traces in LangSmith
After any execution, view traces at:
https://smith.langchain.com/projects/p/agentic-ai-platform

---

## 🔥 Quick Test Commands

### Test All Graphs via Studio
```bash
# Start Studio
./scripts/start_studio.sh

# In browser (http://127.0.0.1:8123):
# 1. Select "chatbot" → type "Hello"
# 2. Select "chatbot_with_tools" → type "What's the weather?"
# 3. Select "research_agent" → enter JSON input
# 4. Select "content_writer" → enter JSON input
```

### Test via Python
```bash
# Create test file
cat > test_all_graphs.py << 'EOF'
from src.agents.graphs.deployable import (
    chatbot_graph,
    chatbot_with_tools_graph,
    research_graph,
    writer_graph
)
from langchain_core.messages import HumanMessage

print("Testing chatbot...")
graph1 = chatbot_graph()
result1 = graph1.invoke({"messages": [HumanMessage(content="Hi")]})
print("✅ Chatbot works!")

print("\nTesting chatbot_with_tools...")
graph2 = chatbot_with_tools_graph()
result2 = graph2.invoke({"messages": [HumanMessage(content="Hi")]})
print("✅ Chatbot with tools works!")

print("\nTesting research_agent...")
graph3 = research_graph()
result3 = graph3.invoke({"query": "AI trends", "max_results": 2})
print("✅ Research agent works!")

print("\nTesting content_writer...")
graph4 = writer_graph()
result4 = graph4.invoke({
    "topic": "AI",
    "content_type": "blog",
    "tone": "casual"
})
print("✅ Content writer works!")

print("\n🎉 All graphs working!")
EOF

# Run tests
uv run python test_all_graphs.py
```

---

## 🐛 Troubleshooting

### Graph not found?
```bash
# Verify graph exists in langgraph.json
cat langgraph.json

# Test import
uv run python -c "from src.agents.graphs.deployable import chatbot_graph; print('✅')"
```

### Studio API not responding?
```bash
# Check if server is running
curl http://127.0.0.1:8123/info

# Check available assistants
curl http://127.0.0.1:8123/assistants
```

### Import errors?
```bash
# Install dependencies
uv sync

# Check Python path
uv run python -c "import sys; print(sys.path)"
```

---

## 📚 More Examples

See these files for detailed examples:
- `docs/LANGGRAPH_STUDIO_GUIDE.md` - Studio usage
- `tests/` - Test files with examples
- `main.py` - FastAPI integration
- `src/api/v1/` - API endpoint examples

---

## 🎊 You're Ready!

Now you know **4 ways** to run your graphs. Start with **Studio UI** for development, then move to **FastAPI** for production!

**Questions?** Check `docs/LANGGRAPH_STUDIO_GUIDE.md`
