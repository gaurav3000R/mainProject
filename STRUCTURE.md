# 📂 Project Structure Overview

## Visual Tree Structure

```
mainProject/
│
├── 📄 main.py                       # FastAPI application entry point
├── 📄 run.py                        # Alternative server runner
├── 📄 pyproject.toml                # UV dependencies & tool config
├── 📄 uv.lock                       # Dependency lock file
├── 📄 .env                          # Environment variables (git-ignored)
├── 📄 .env.example                  # Environment template
├── 📄 README.md                     # Main documentation
├── 📄 PROJECT_SUMMARY.md            # This creation summary
├── 📄 STRUCTURE.md                  # This file
│
├── 📁 src/                          # Source code
│   ├── __init__.py
│   │
│   ├── 📁 core/                     # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                # Settings with Pydantic
│   │   └── exceptions.py            # Custom exception classes
│   │
│   ├── 📁 llms/                     # LLM providers
│   │   ├── __init__.py
│   │   └── base.py                  # BaseLLM, GroqLLM, OpenAILLM, Factory
│   │
│   ├── 📁 tools/                    # Agent tools
│   │   ├── __init__.py
│   │   └── base.py                  # Search, calculator, tool node
│   │
│   ├── 📁 agents/                   # Agent workflows
│   │   ├── __init__.py
│   │   │
│   │   ├── 📁 states/              # State schemas
│   │   │   ├── __init__.py
│   │   │   └── base.py             # AgentState, ChatbotState, etc.
│   │   │
│   │   ├── 📁 nodes/               # Graph node functions
│   │   │   ├── __init__.py
│   │   │   └── base.py             # ChatbotNode, ResearchNode, WriterNode
│   │   │
│   │   └── 📁 graphs/              # Graph builders
│   │       ├── __init__.py
│   │       └── base.py             # GraphFactory & builders
│   │
│   ├── 📁 schemas/                  # Pydantic models
│   │   ├── __init__.py
│   │   └── api.py                  # Request/Response schemas
│   │
│   ├── 📁 api/                      # FastAPI layer
│   │   ├── __init__.py
│   │   ├── dependencies.py          # Dependency injection
│   │   │
│   │   ├── 📁 v1/                  # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Chat endpoints
│   │   │   ├── research.py         # Research agent endpoint
│   │   │   ├── writer.py           # Content writer endpoint
│   │   │   └── health.py           # Health check & info
│   │   │
│   │   └── 📁 middlewares/         # Custom middlewares
│   │       ├── __init__.py
│   │       └── base.py             # Logging, Error, RateLimit, CORS
│   │
│   ├── 📁 utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py               # Loguru logging setup
│   │   └── helpers.py              # Helper functions (JWT, hashing, etc.)
│   │
│   └── 📁 services/                 # Business logic (extensible)
│       └── __init__.py
│
├── 📁 tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration & fixtures
│   │
│   ├── 📁 unit/                    # Unit tests
│   │   ├── __init__.py
│   │   └── test_llms.py            # LLM factory tests
│   │
│   ├── 📁 integration/             # Integration tests
│   │   ├── __init__.py
│   │   └── test_api.py             # API endpoint tests
│   │
│   └── 📁 e2e/                     # End-to-end tests
│       └── __init__.py
│
├── 📁 docs/                         # Documentation
│   ├── ARCHITECTURE.md              # System architecture details
│   └── QUICKSTART.md               # Quick start guide
│
├── 📁 scripts/                      # Utility scripts
│   ├── dev.sh                       # Development startup script
│   ├── test.sh                      # Run tests script
│   └── lint.sh                      # Code quality check script
│
├── 📁 logs/                         # Application logs (auto-created)
│   ├── app_YYYY-MM-DD.log          # Daily application logs
│   └── error_YYYY-MM-DD.log        # Daily error logs
│
└── 📁 data/                         # Data storage
    ├── 📁 raw/                     # Raw data
    └── 📁 processed/               # Processed data
```

## 📊 File Count Summary

| Category | Count | Description |
|----------|-------|-------------|
| Python Source Files | 30+ | Main application code |
| Test Files | 4+ | Unit & integration tests |
| Documentation Files | 5+ | README, guides, architecture |
| Configuration Files | 4+ | pyproject.toml, .env, etc. |
| Scripts | 3 | Development utilities |
| Total Lines of Code | 3,500+ | Including comments & docs |

## 🎯 Key File Descriptions

### Entry Points
- **main.py**: FastAPI application with all routes and middlewares
- **run.py**: Alternative runner with custom uvicorn config

### Core Configuration
- **src/core/config.py**: Environment-based settings using Pydantic
- **src/core/exceptions.py**: Custom exception hierarchy

### LLM Layer
- **src/llms/base.py**: 
  - `BaseLLM` abstract class
  - `GroqLLM` and `OpenAILLM` implementations
  - `LLMFactory` for creating LLM instances

### Agent Layer
- **src/agents/states/base.py**: TypedDict schemas for different agents
- **src/agents/nodes/base.py**: Node functions (ChatbotNode, ResearchNode, WriterNode)
- **src/agents/graphs/base.py**: Graph builders and factory

### API Layer
- **src/api/v1/*.py**: RESTful endpoints for each agent type
- **src/api/middlewares/base.py**: Custom middlewares (logging, errors, rate limiting)
- **src/api/dependencies.py**: FastAPI dependency injection

### Utilities
- **src/utils/logger.py**: Loguru logging configuration
- **src/utils/helpers.py**: JWT, password hashing, sanitization

### Testing
- **tests/conftest.py**: Pytest fixtures and configuration
- **tests/unit/**: Unit tests for individual components
- **tests/integration/**: API endpoint integration tests

## 🔄 Request Flow

```
HTTP Request
    ↓
Middleware Layer (logging, rate limiting)
    ↓
FastAPI Router
    ↓
Dependency Injection (get LLM, build graph)
    ↓
Graph Execution (nodes process state)
    ↓
LLM Provider (Groq/OpenAI)
    ↓
Response Processing
    ↓
Middleware Layer (headers, logging)
    ↓
HTTP Response
```

## 🧩 Module Dependencies

```
main.py
├── src.api.v1.*           (API endpoints)
├── src.api.middlewares.*  (Middlewares)
└── src.core.config        (Settings)

API Endpoints
├── src.agents.graphs.*    (Graph builders)
├── src.llms.base          (LLM providers)
├── src.schemas.api        (Request/Response models)
└── src.api.dependencies   (Dependency injection)

Graph Builders
├── src.agents.nodes.*     (Node functions)
├── src.agents.states.*    (State schemas)
└── src.tools.base         (Tools)

Nodes
├── src.llms.base          (LLM invocation)
└── src.tools.base         (Tool execution)
```

## 🎨 Design Patterns Used

1. **Factory Pattern**: LLMFactory, GraphFactory
2. **Strategy Pattern**: Different agent strategies
3. **Dependency Injection**: FastAPI DI system
4. **Middleware Pattern**: Request/response processing
5. **Builder Pattern**: Graph construction
6. **Singleton Pattern**: Settings caching

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| pyproject.toml | UV dependencies, tool configs (black, ruff, mypy, pytest) |
| .env | Environment variables (API keys, settings) |
| .env.example | Template for environment variables |
| .gitignore | Git ignore rules |
| uv.lock | Dependency lock file (auto-generated) |

## 🚀 Quick Navigation

- **Want to add a new endpoint?** → `src/api/v1/`
- **Want to add a new agent?** → `src/agents/`
- **Want to add a new LLM?** → `src/llms/base.py`
- **Want to add a new tool?** → `src/tools/base.py`
- **Want to change settings?** → `.env` or `src/core/config.py`
- **Want to add tests?** → `tests/unit/` or `tests/integration/`

---

**Generated**: November 2024
**Version**: 1.0.0
**Maintainer**: Agentic AI Team
