# 🎯 LangGraph Commands Cheat Sheet

Quick reference for running your graphs in different ways.

---

## 🚀 Quick Start

```bash
# Start Studio (Visual UI)
./scripts/start_studio.sh

# Test all graphs in Python
uv run python scripts/test_graphs.py

# Start FastAPI server
uv run python main.py
```

---

## 1️⃣ LangGraph Studio (Visual)

### Start Server
```bash
# Default port 8123
uv run langgraph dev

# Custom port
uv run langgraph dev --port 8124

# With public tunnel
uv run langgraph dev --tunnel

# With debugging
uv run langgraph dev --debug-port 5678
```

### Access
- **Studio UI**: http://127.0.0.1:8123
- **LangSmith**: https://smith.langchain.com

---

## 2️⃣ Studio API (HTTP)

Server must be running first: `uv run langgraph dev`

### Chatbot
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "chatbot",
    "input": {"messages": [{"role": "user", "content": "Hello"}]},
    "config": {"configurable": {"thread_id": "test-1"}}
  }'
```

### Chatbot with Tools
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "chatbot_with_tools",
    "input": {"messages": [{"role": "user", "content": "Search for AI news"}]},
    "config": {"configurable": {"thread_id": "test-2"}}
  }'
```

### Research Agent
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "research_agent",
    "input": {"query": "AI trends", "max_results": 5},
    "config": {"configurable": {"thread_id": "test-3"}}
  }'
```

### Content Writer
```bash
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "content_writer",
    "input": {
      "topic": "AI Agents",
      "content_type": "blog",
      "tone": "professional"
    },
    "config": {"configurable": {"thread_id": "test-4"}}
  }'
```

### Utility Endpoints
```bash
# List available graphs
curl http://127.0.0.1:8123/assistants

# Get server info
curl http://127.0.0.1:8123/info

# Health check
curl http://127.0.0.1:8123/health
```

---

## 3️⃣ Python Direct Import

### Basic Execution
```python
from src.agents.graphs.deployable import chatbot_graph
from langchain_core.messages import HumanMessage

graph = chatbot_graph()
result = graph.invoke({
    "messages": [HumanMessage(content="Hello!")]
})
print(result["messages"][-1].content)
```

### With Streaming
```python
from src.agents.graphs.deployable import chatbot_graph
from langchain_core.messages import HumanMessage

graph = chatbot_graph()
input_data = {"messages": [HumanMessage(content="Tell me a story")]}

for chunk in graph.stream(input_data):
    print(chunk)
```

### With Checkpointing (Memory)
```python
from langgraph.checkpoint.memory import MemorySaver
from src.agents.graphs.deployable import chatbot_graph

# Add memory
memory = MemorySaver()
graph = chatbot_graph()  # Then re-compile with checkpointer

config = {"configurable": {"thread_id": "user-123"}}
result = graph.invoke(input_data, config=config)
```

### Run from Command Line
```bash
# Quick one-liner
uv run python -c "
from src.agents.graphs.deployable import chatbot_graph
from langchain_core.messages import HumanMessage
graph = chatbot_graph()
result = graph.invoke({'messages': [HumanMessage(content='Hi')]})
print(result['messages'][-1].content)
"

# Run test script
uv run python scripts/test_graphs.py
```

---

## 4️⃣ FastAPI Endpoints

Start server: `uv run python main.py`

### Chatbot (Simple)
```bash
curl -X POST http://localhost:8000/api/v1/chat/simple \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### Chatbot (With Tools)
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the latest AI news?"}'
```

### Research Agent
```bash
curl -X POST http://localhost:8000/api/v1/research/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Impact of AI on healthcare",
    "max_results": 5
  }'
```

### Content Writer
```bash
curl -X POST http://localhost:8000/api/v1/writer/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Future of AI",
    "content_type": "blog",
    "tone": "professional"
  }'
```

---

## 🔍 Debugging & Monitoring

### View Logs
```bash
# Studio logs
tail -f logs/app.log

# FastAPI logs (if running)
tail -f logs/app.log
```

### Check LangSmith Traces
```bash
# Verify connection
uv run python -c "from src.utils.langsmith import verify_langsmith_connection; verify_langsmith_connection()"

# View traces
open https://smith.langchain.com/projects/p/agentic-ai-platform
```

### Debug Graph Structure
```python
# View graph structure
from src.agents.graphs.deployable import chatbot_graph

graph = chatbot_graph()
print(graph.get_graph().draw_ascii())
```

---

## 🛠️ Development Workflow

### Typical Development Flow
```bash
# Terminal 1: Start Studio with hot-reload
uv run langgraph dev --port 8123

# Terminal 2: Edit code
# Your IDE or editor

# Terminal 3: Run tests
uv run pytest tests/

# Terminal 4: Monitor logs
tail -f logs/app.log
```

### Quick Test Cycle
```bash
# 1. Make code changes
vim src/agents/nodes/base.py

# 2. Studio auto-reloads (if running)
# OR test directly:
uv run python scripts/test_graphs.py

# 3. Check LangSmith for traces
open https://smith.langchain.com
```

---

## 📊 Input/Output Formats

### Chatbot
```python
# Input
{
    "messages": [
        {"role": "user", "content": "Your message here"}
    ]
}

# Output
{
    "messages": [
        # ... conversation history
        {"role": "assistant", "content": "Response here"}
    ]
}
```

### Research Agent
```python
# Input
{
    "query": "Your research topic",
    "max_results": 5
}

# Output
{
    "query": "Your research topic",
    "sources": [...],
    "summary": "Research summary here"
}
```

### Content Writer
```python
# Input
{
    "topic": "Your topic",
    "content_type": "blog",  # or "article", "social"
    "tone": "professional"   # or "casual", "formal"
}

# Output
{
    "topic": "Your topic",
    "outline": "Content outline",
    "draft": "Draft content",
    "final_content": "Polished final content"
}
```

---

## 🚨 Common Issues

### Port Already in Use
```bash
# Check what's using the port
lsof -i :8123

# Use different port
uv run langgraph dev --port 8124
```

### Import Errors
```bash
# Sync dependencies
uv sync

# Check Python path
uv run python -c "import sys; print('\n'.join(sys.path))"
```

### Graph Not Found
```bash
# List available graphs
cat langgraph.json | jq '.graphs'

# Test import
uv run python -c "from src.agents.graphs.deployable import chatbot_graph; print('✅')"
```

### LangSmith Not Tracing
```bash
# Check environment
cat .env | grep LANGCHAIN

# Verify connection
uv run python -c "from src.utils.langsmith import verify_langsmith_connection; verify_langsmith_connection()"
```

---

## 💡 Pro Tips

```bash
# Run in background with nohup
nohup uv run langgraph dev > studio.log 2>&1 &

# Use jq for pretty JSON
curl http://127.0.0.1:8123/assistants | jq .

# Test with different models
DEFAULT_MODEL=gpt-4 uv run python scripts/test_graphs.py

# Monitor system resources
watch -n 1 'ps aux | grep langgraph'
```

---

## 📚 Related Documentation

- `docs/LANGGRAPH_STUDIO_GUIDE.md` - Full Studio guide
- `docs/HOW_TO_RUN_GRAPHS.md` - Detailed examples
- `QUICK_START.md` - Get started in 3 steps
- `README.md` - Project overview

---

## 🎯 Most Common Commands

```bash
# Start visual debugging
./scripts/start_studio.sh

# Test all graphs
uv run python scripts/test_graphs.py

# Start production API
uv run python main.py

# View traces
open https://smith.langchain.com
```

---

**Happy Graph Running! 🚀**
