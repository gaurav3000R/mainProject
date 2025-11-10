# 🚀 Quick Start Guide - LangGraph Studio & LangSmith

## ✅ Setup Complete!

Your Agentic AI platform is now fully integrated with LangGraph Studio and LangSmith for visual debugging and tracing.

---

## 🎯 Start Developing in 3 Steps

### Step 1: Start LangGraph Studio
```bash
cd mainProject
./scripts/start_studio.sh
```

**What happens:**
- Dev server starts on http://127.0.0.1:8123
- All 4 graphs are available
- Hot-reload enabled for instant updates

### Step 2: Open Studio in Browser
```
http://127.0.0.1:8123
```

**Select a graph:**
- `chatbot` - Simple conversation
- `chatbot_with_tools` - Chat with web search
- `research_agent` - Research workflow
- `content_writer` - Content generation

### Step 3: Test & Debug
1. Type a message in the chat interface
2. Watch the graph execute node by node
3. Inspect state at each step
4. View tool calls in real-time
5. Check traces in LangSmith

---

## 📊 View Traces in LangSmith

1. Go to: https://smith.langchain.com
2. Select project: **agentic-ai-platform**
3. View all runs, metrics, and traces
4. Debug errors with detailed logs

---

## 🎨 What You Can Do Now

### Visual Debugging
✅ See graph flow visually  
✅ Step through execution  
✅ Inspect state changes  
✅ Debug tool calls  
✅ Test different inputs  

### Performance Monitoring
✅ Track latency per node  
✅ Monitor token usage  
✅ Measure costs  
✅ Compare runs  
✅ Set up alerts  

### Development Workflow
✅ Edit code → Auto-reload  
✅ Test in Studio UI  
✅ Check traces in LangSmith  
✅ Iterate quickly  
✅ Deploy with confidence  

---

## 📚 Documentation

- **Studio Guide**: `docs/LANGGRAPH_STUDIO_GUIDE.md` - Complete usage guide
- **Setup Details**: `docs/SETUP_COMPLETE.md` - What was configured
- **Learning Path**: `LEARNING_PATH.md` - 18 weeks of content
- **Main README**: `README.md` - Full project documentation

---

## 🔥 Quick Commands

```bash
# Start Studio (recommended)
./scripts/start_studio.sh

# Start Studio manually
uv run langgraph dev --port 8123

# Start with public tunnel
uv run langgraph dev --tunnel

# Start with debugging
uv run langgraph dev --debug-port 5678

# Start FastAPI (separate terminal)
uv run python main.py

# Run tests
uv run pytest

# Check setup
uv run python -c "from src.utils.langsmith import verify_langsmith_connection; verify_langsmith_connection()"
```

---

## 🎓 Learning Resources

### Videos & Tutorials
- LangGraph Studio Overview
- Debugging Agents Visually
- Optimizing Token Usage
- Multi-Agent Workflows

### Key Topics Covered in LEARNING_PATH.md
1. **Beginner**: Basic chatbots, state management
2. **Intermediate**: Tools, routing, memory
3. **Advanced**: RAG, corrective RAG, agentic RAG
4. **Expert**: Multi-agent systems, human-in-loop
5. **Production**: Scalability, monitoring, deployment

---

## 💡 Pro Tips

1. **Keep Studio Running**: It's your visual debugger
2. **Use Thread IDs**: Track multi-turn conversations
3. **Check LangSmith Daily**: Monitor performance trends
4. **Save Good Traces**: Bookmark examples in LangSmith
5. **Iterate Fast**: Hot-reload makes development rapid

---

## 🐛 Troubleshooting

### Studio won't start?
```bash
# Check if port is in use
lsof -i :8123
# Or use different port
uv run langgraph dev --port 8124
```

### Graphs not showing?
```bash
# Verify configuration
cat langgraph.json
uv run python -c "from src.agents.graphs.deployable import chatbot_graph; chatbot_graph()"
```

### No traces in LangSmith?
```bash
# Check environment
cat .env | grep LANGCHAIN
# Verify connection
uv run python -c "from src.utils.langsmith import verify_langsmith_connection; verify_langsmith_connection()"
```

---

## 🎊 You're Ready!

**Everything is configured and tested:**
- ✅ 4 graphs ready to use
- ✅ LangSmith tracing active
- ✅ Studio server working
- ✅ Hot-reload enabled
- ✅ Documentation complete

**Start building amazing agents!** 🚀

Questions? Check `docs/LANGGRAPH_STUDIO_GUIDE.md` for detailed help.
