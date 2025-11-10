# 🎯 LangGraph Studio & CLI Integration Guide

## 📋 Overview

This guide helps you visualize and debug your LangGraph agents using LangGraph Studio and CLI.

## 🚀 Quick Start

### 1. **Install LangGraph CLI** (Already done ✅)
```bash
uv add langgraph-cli
```

### 2. **Start Development Server**
```bash
# Start the LangGraph dev server
uv run langgraph dev

# Or specify port
uv run langgraph dev --port 8123

# With debug mode
uv run langgraph dev --debug-port 5678 --wait-for-client
```

The server will start on `http://127.0.0.1:8123` by default and automatically open LangGraph Studio in your browser.

### 3. **Access LangGraph Studio**
- Local: `http://127.0.0.1:8123`
- LangSmith Studio: `https://smith.langchain.com/studio`

## 📁 Project Configuration

### `langgraph.json`
```json
{
  "dependencies": ["."],
  "graphs": {
    "chatbot": "./src/agents/graphs/deployable.py:chatbot_graph",
    "chatbot_with_tools": "./src/agents/graphs/deployable.py:chatbot_with_tools_graph",
    "research_agent": "./src/agents/graphs/deployable.py:research_graph",
    "content_writer": "./src/agents/graphs/deployable.py:writer_graph"
  },
  "env": ".env"
}
```

### Available Graphs

| Graph Name | Description | Endpoint |
|------------|-------------|----------|
| `chatbot` | Simple conversational bot | Basic chat with memory |
| `chatbot_with_tools` | Chat with web search | Tools + conditional routing |
| `research_agent` | Research and summarize | Multi-step research workflow |
| `content_writer` | Content generation | Outline → Draft → Polish |

## 🎨 Using LangGraph Studio

### Visual Debugging Features

1. **Graph Visualization**
   - See your graph nodes and edges visually
   - Understand the flow of your agent
   - Identify routing decisions

2. **Step-by-Step Execution**
   - Run agents step by step
   - Inspect state at each node
   - See tool calls and responses

3. **State Inspection**
   - View state transformations
   - Debug data flow
   - Identify issues in your logic

4. **Interactive Testing**
   - Test different inputs
   - Modify state manually
   - See real-time results

### How to Use Studio

1. **Start the dev server:**
   ```bash
   uv run langgraph dev
   ```

2. **Select a graph** from the dropdown (chatbot, research_agent, etc.)

3. **Input your message** in the chat interface

4. **Watch the execution:**
   - See which nodes are triggered
   - View state changes
   - Inspect tool calls

5. **Debug issues:**
   - Click on nodes to see state
   - View error messages
   - Modify and retry

## 🔍 Testing Your Graphs

### Using the Studio UI

1. **Basic Chatbot Test**
   ```
   Graph: chatbot
   Input: "Hello, how are you?"
   Expected: Simple conversational response
   ```

2. **Chatbot with Tools Test**
   ```
   Graph: chatbot_with_tools
   Input: "What's the latest news about AI?"
   Expected: Web search → Tool execution → Response with info
   ```

3. **Research Agent Test**
   ```
   Graph: research_agent
   Input: {"query": "Latest developments in LangChain", "max_results": 5}
   Expected: Search → Summarize → Comprehensive report
   ```

4. **Content Writer Test**
   ```
   Graph: content_writer
   Input: {
     "topic": "Introduction to LangGraph",
     "content_type": "blog",
     "tone": "professional"
   }
   Expected: Outline → Draft → Polished content
   ```

### Using API Directly

When the dev server is running, you can also call the API:

```bash
# List available graphs
curl http://127.0.0.1:8123/info

# Invoke a graph
curl -X POST http://127.0.0.1:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "chatbot",
    "input": {
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    },
    "config": {
      "configurable": {
        "thread_id": "test-thread-1"
      }
    }
  }'
```

## 🔗 LangSmith Integration

Your graphs automatically trace to LangSmith when running in dev mode.

### View Traces

1. Go to [LangSmith](https://smith.langchain.com)
2. Select your project: `agentic-ai-platform`
3. View traces for each run
4. Debug issues with detailed logs

### Key Metrics to Monitor

- **Latency**: How long each node takes
- **Token Usage**: LLM call costs
- **Tool Calls**: Which tools are used
- **Error Rates**: Failed runs
- **State Flow**: Data transformations

## 🛠️ Advanced Features

### 1. **Hot Reloading**
Changes to your code automatically reload the server:
```bash
uv run langgraph dev  # Auto-reload enabled by default
```

### 2. **Remote Debugging**
Debug your code with debugpy:
```bash
uv run langgraph dev --debug-port 5678 --wait-for-client
```

Then attach your IDE debugger to port 5678.

### 3. **Public Tunneling**
Share your local graph with others:
```bash
uv run langgraph dev --tunnel
```

This creates a public URL via Cloudflare tunnel.

### 4. **Multiple Workers**
Handle concurrent requests:
```bash
uv run langgraph dev --n-jobs-per-worker 20
```

## 📊 Example Workflows

### Workflow 1: Debug a Failing Agent

1. Start dev server: `uv run langgraph dev`
2. Select failing graph in Studio
3. Input the problematic query
4. Step through execution
5. Inspect state at failure point
6. Fix the code (auto-reloads)
7. Test again

### Workflow 2: Optimize Token Usage

1. Run agent in Studio
2. Check LangSmith traces
3. Identify expensive nodes
4. Optimize prompts
5. Compare before/after metrics

### Workflow 3: Test New Features

1. Add new node to graph
2. Server auto-reloads
3. Test in Studio UI
4. Verify state changes
5. Commit working code

## 🔧 Troubleshooting

### Issue: "No graphs found"
**Solution**: Check `langgraph.json` paths are correct
```bash
# Verify paths exist
ls -la src/agents/graphs/deployable.py
```

### Issue: "Import errors"
**Solution**: Ensure all dependencies are installed
```bash
uv sync
```

### Issue: "Port already in use"
**Solution**: Use different port
```bash
uv run langgraph dev --port 8124
```

### Issue: "Environment variables not loaded"
**Solution**: Check `.env` file exists and is in project root
```bash
ls -la .env
cat .env | grep GROQ_API_KEY
```

## 📚 Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangGraph Studio Guide](https://langchain-ai.github.io/langgraph/cloud/concepts/langgraph_studio/)
- [LangSmith Tracing](https://docs.smith.langchain.com/)
- [Debugging Guide](https://langchain-ai.github.io/langgraph/how-tos/debug/)

## 🎯 Next Steps

1. ✅ Start dev server and test all graphs
2. 📊 Monitor traces in LangSmith
3. 🔍 Debug any issues visually
4. 🚀 Deploy with `langgraph up` when ready
5. 📈 Set up monitoring and alerts

---

**Pro Tip**: Keep the dev server running while developing. The hot-reload feature makes iteration super fast! 🚀
