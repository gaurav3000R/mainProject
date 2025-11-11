# Agentic AI Platform 🤖

A production-ready, modular Agentic AI platform built with **LangGraph**, **FastAPI**, and **UV** package manager.

## 🚀 Features

- **Multiple Agent Types**: Chatbot, Research Agent, Content Writer
- **Tool Integration**: Web search, Calculator, Custom tools
- **LLM Support**: Groq, OpenAI (extensible)
- **Production Ready**: Logging, error handling, rate limiting, CORS
- **Type Safe**: Pydantic validation throughout
- **Modern Stack**: UV for dependencies, FastAPI for APIs
- **Modular Architecture**: Clean separation of concerns
- **Testing**: Unit and integration tests included

## 📁 Project Structure

```
mainProject/
├── src/
│   ├── core/              # Configuration and exceptions
│   ├── llms/              # LLM providers (Groq, OpenAI)
│   ├── tools/             # Agent tools (search, calculator)
│   ├── agents/
│   │   ├── nodes/         # Graph node functions
│   │   ├── states/        # State schemas
│   │   └── graphs/        # Graph builders
│   ├── schemas/           # Pydantic models
│   ├── api/
│   │   ├── v1/            # API endpoints
│   │   └── middlewares/   # Custom middlewares
│   └── utils/             # Helper functions
├── tests/                 # Unit & integration tests
├── logs/                  # Application logs
├── data/                  # Data storage
├── main.py                # FastAPI application
└── pyproject.toml         # UV dependencies
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# 1. Navigate to project
cd mainProject

# 2. Install dependencies (UV handles venv automatically)
uv sync

# 3. Copy environment file
cp .env.example .env

# 4. Add your API keys to .env
# - GROQ_API_KEY (required)
# - TAVILY_API_KEY (for web search)
# - OPENAI_API_KEY (optional)
```

### Run the Server

```bash
# Development mode with auto-reload
uv run python main.py

# Or use uvicorn directly
uv run uvicorn main:app --reload --port 8000
```

🎉 **API is live at**: http://localhost:8000
📚 **Interactive docs**: http://localhost:8000/docs

### Run LangGraph Studio (Visual Debugging)

```bash
# Start LangGraph dev server with Studio
./scripts/start_studio.sh

# Or manually
uv run langgraph dev --port 8123
```

🎨 **LangGraph Studio**: http://127.0.0.1:8123  
📊 **LangSmith Traces**: https://smith.langchain.com/projects/p/agentic-ai-platform

See [LangGraph Studio Guide](./docs/LANGGRAPH_STUDIO_GUIDE.md) for detailed usage.

## 📡 API Examples

### 1. Simple Chat
```bash
curl -X POST "http://localhost:8000/api/v1/chat/simple" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing in simple terms"}'
```

### 2. Chat with Web Search
```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the latest AI developments in 2024?"}'
```

### 3. Research Agent
```bash
curl -X POST "http://localhost:8000/api/v1/research/" \
  -H "Content-Type: application/json" \
  -d '{"query": "Impact of AI on healthcare", "max_results": 5}'
```

### 4. Content Writer
```bash
curl -X POST "http://localhost:8000/api/v1/writer/" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Future of Artificial Intelligence",
    "content_type": "blog",
    "tone": "professional"
  }'
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# With coverage report
uv run pytest --cov=src --cov-report=html

# Run specific tests
uv run pytest tests/unit/
uv run pytest tests/integration/
```

## 🔧 Development

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/

# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

## 🏗️ Architecture

### Three-Layer Design

1. **LLM Layer** (`src/llms/`)
   - Abstract `BaseLLM` interface
   - Factory pattern for provider creation
   - Easy to extend with new providers

2. **Agent Layer** (`src/agents/`)
   - **States**: Type-safe schemas with TypedDict
   - **Nodes**: Pure functions for graph operations
   - **Graphs**: LangGraph workflow builders
   - **Tools**: Modular tool integration

3. **API Layer** (`src/api/`)
   - FastAPI with async support
   - Pydantic validation
   - Custom middlewares
   - Dependency injection

## 🔐 Configuration

All settings in `.env`:
```bash
# Required
GROQ_API_KEY=your_key_here

# Optional (enables features)
TAVILY_API_KEY=for_web_search
OPENAI_API_KEY=alternative_llm
LANGCHAIN_API_KEY=for_tracing

# Server
PORT=8000
ENVIRONMENT=development
DEBUG=true
```

## 📊 Available Agents

| Agent Type | Description | Endpoint |
|------------|-------------|----------|
| **Simple Chatbot** | Basic conversational AI | `/api/v1/chat/simple` |
| **Chatbot with Tools** | Chat with web search | `/api/v1/chat/` |
| **Research Agent** | Search & summarize info | `/api/v1/research/` |
| **Content Writer** | Create structured content | `/api/v1/writer/` |

## 🎯 Key Features

### Factory Pattern
```python
from src.llms.base import LLMFactory

# Create LLM dynamically
llm = LLMFactory.create(provider="groq", model_name="qwen/qwen3-32b")
```

### Graph Builder
```python
from src.agents.graphs.base import GraphFactory

# Build graph workflow
graph = GraphFactory.create("research", llm)
result = graph.invoke({"query": "AI trends"})
```

### Dependency Injection
```python
from src.api.dependencies import get_llm

@router.post("/endpoint")
async def endpoint(llm: BaseLLM = Depends(get_llm)):
    # LLM automatically injected
    pass
```

## 🚀 Production Checklist

- [ ] Set strong `SECRET_KEY` in `.env`
- [ ] Configure proper CORS origins
- [ ] Enable rate limiting
- [ ] Set `ENVIRONMENT=production`
- [ ] Use production-grade database
- [ ] Add monitoring/observability
- [ ] Configure reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Review security headers

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🤝 Extending the Platform

### Add New LLM Provider
```python
# src/llms/custom.py
from src.llms.base import BaseLLM

class CustomLLM(BaseLLM):
    def get_client(self):
        # Implement your LLM client
        pass

# Register it
LLMFactory.register_provider("custom", CustomLLM)
```

### Add New Agent Type
```python
# src/agents/graphs/custom.py
class CustomGraphBuilder:
    def build(self):
        # Build your custom graph
        pass

# Register it
GraphFactory.register_builder("custom", CustomGraphBuilder)
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Run `uv sync` |
| API key errors | Check `.env` file |
| Port in use | Change `PORT` in `.env` |
| Module not found | Ensure you're in project root |

## 📝 License

MIT License - See LICENSE file

## 🙏 Built With

- [LangChain](https://langchain.com/) - LLM framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent workflows
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [UV](https://github.com/astral-sh/uv) - Package manager
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Groq](https://groq.com/) - Fast LLM inference

---

**⭐ Star this repo if you find it helpful!**

Made with ❤️ using LangGraph, FastAPI, and UV
