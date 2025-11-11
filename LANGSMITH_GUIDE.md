# LangSmith Tracing Guide

## ✅ Status: WORKING

LangSmith tracing is properly configured and operational for all graphs.

## 📋 Configuration

### Environment Variables (.env)

```bash
# LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=agentic-ai-platform
```

### Current Setup

Your project is already configured with:
- ✅ LangSmith enabled in `src/core/config.py`
- ✅ Auto-setup on import via `setup_langsmith()`
- ✅ Connection verification in `src/utils/langsmith.py`
- ✅ Integrated in FastAPI app startup (`main.py`)

## 🧪 Verification

### Quick Test

```bash
python verify_langsmith.py
```

This will:
1. Verify LangSmith connection
2. Run a test graph execution
3. Confirm traces are being sent
4. Show your dashboard URL

### Full Graph Testing

```bash
python test_langsmith_tracing.py
```

Tests all 6 graphs and verifies tracing for each.

## 🔗 Viewing Traces

### Dashboard URL
```
https://api.smith.langchain.com/projects/p/agentic-ai-platform
```

Or get it programmatically:
```python
from src.utils.langsmith import get_langsmith_url
print(get_langsmith_url())
```

### What You'll See

Each graph execution creates a trace showing:
- **Graph Structure**: Visual representation of your LangGraph workflow
- **Node Executions**: Each node's input/output
- **LLM Calls**: Model requests, responses, tokens used
- **Tool Invocations**: Tool calls and results
- **Timing**: Execution duration for each step
- **Errors**: Stack traces if anything fails

## 📊 Traced Graphs

All 6 graphs are automatically traced:

1. **chatbot** - Simple conversational agent
2. **chatbot_with_tools** - Chatbot with web search
3. **research_agent** - Multi-step research workflow
4. **content_writer** - Content generation pipeline
5. **news_summarization** - News fetching and summarization
6. **redmine_chatbot** - Adaptive RAG Redmine assistant

## 🚀 Usage Examples

### Method 1: Automatic Tracing (Current Setup)

```python
from langchain_core.messages import HumanMessage
from src.agents.graphs.deployable import chatbot_graph

# Tracing is automatic - just use the graph
graph = chatbot_graph()
result = graph.invoke({
    "messages": [HumanMessage(content="Hello!")]
})

# Traces are automatically sent to LangSmith
```

### Method 2: @traceable Decorator

For custom functions you want to trace:

```python
from langsmith import traceable

@traceable(name="my_function", run_type="chain")
def process_data(data: dict) -> dict:
    # Your code here
    return {"processed": data}

# Automatically traced!
result = process_data({"key": "value"})
```

### Method 3: RunTree (Manual Control)

For fine-grained control:

```python
from langsmith.run_trees import RunTree

# Create parent run
run = RunTree(
    name="My Workflow",
    run_type="chain",
    inputs={"data": "input"},
    tags=["production"]
)
run.post()

try:
    # Your code here
    result = {"output": "data"}
    run.end(outputs=result)
finally:
    run.patch()
```

### Method 4: trace() Context Manager

For tracing code blocks:

```python
from langsmith import trace

with trace(name="Data Pipeline", run_type="chain"):
    # Your code here
    result = process_data()
```

### See Full Examples

Run the comprehensive demo:
```bash
python examples/langsmith_annotations.py
```

### FastAPI Endpoints

All API endpoints automatically trace:

```bash
# Chat endpoint
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Research endpoint
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d '{"query": "Python programming"}'

# Each request creates a trace in LangSmith
```

### With Custom Run Name

```python
from langchain_core.runnables import RunnableConfig

result = graph.invoke(
    state,
    config=RunnableConfig(
        run_name="My Custom Run",
        tags=["production", "important"]
    )
)
```

## 🔧 Troubleshooting

### Traces Not Appearing

**Check 1: Environment Variables**
```bash
python -c "import os; from src.core.config import settings, setup_langsmith; setup_langsmith(); print('Tracing:', os.getenv('LANGCHAIN_TRACING_V2')); print('Project:', os.getenv('LANGCHAIN_PROJECT'))"
```

**Check 2: API Key**
```bash
python -c "from src.utils.langsmith import verify_langsmith_connection; verify_langsmith_connection()"
```

**Check 3: Network**
- Ensure you can reach `https://api.smith.langchain.com`
- Check firewall/proxy settings

### Common Issues

#### "LangSmith is not enabled"
- Set `LANGCHAIN_TRACING_V2=true` in `.env`
- Restart your application

#### "Connection failed"
- Verify `LANGCHAIN_API_KEY` is correct
- Check API key permissions in LangSmith dashboard

#### "Project not found"
- The project will be auto-created on first connection
- Or create manually in LangSmith dashboard

#### Traces delayed
- LangSmith traces may take 5-10 seconds to appear
- Refresh the dashboard page
- Check "All" filter if using project filters

## 📈 Best Practices

### 1. Use Meaningful Run Names
```python
config = RunnableConfig(run_name=f"redmine_query_{user_id}")
```

### 2. Add Tags
```python
config = RunnableConfig(
    tags=["production", "user_facing", "high_priority"]
)
```

### 3. Add Metadata
```python
config = RunnableConfig(
    metadata={
        "user_id": "12345",
        "session_id": "abc-def",
        "version": "v1.0"
    }
)
```

### 4. Monitor Performance
- Check average response times
- Identify slow nodes
- Optimize based on trace data

### 5. Debug with Traces
- View exact inputs/outputs for each node
- See why tool calls are made
- Understand decision-making flow

## 🔒 Security Notes

- ✅ API keys stored in `.env` (not committed to git)
- ✅ `.env` is in `.gitignore`
- ✅ Use different projects for dev/staging/prod
- ✅ Rotate API keys periodically

## 📚 Additional Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Tracing Guide](https://docs.smith.langchain.com/tracing)
- [LangGraph Tracing](https://langchain-ai.github.io/langgraph/how-tos/tracing/)

## 🎯 Summary

**Your LangSmith tracing is working correctly!**

- ✅ Configuration: Complete
- ✅ Connection: Verified
- ✅ Graphs: All 6 traced
- ✅ Dashboard: Accessible

Just use your graphs normally - tracing happens automatically.

View traces at: https://api.smith.langchain.com/projects/p/agentic-ai-platform
