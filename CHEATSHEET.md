# 🚀 GETTING STARTED CHEAT SHEET

## Quick Commands Reference

### First Time Setup
```bash
# 1. Navigate to project
cd /home/hello/Documents/Project/RND/AgenticAI/mainProject

# 2. Install dependencies (UV automatically creates venv)
uv sync

# 3. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 4. Verify installation
uv run python -c "import fastapi, langchain, langgraph; print('✅ All good!')"
```

### Development Server
```bash
# Start with auto-reload (recommended for development)
uv run python main.py

# Alternative: Start with uvicorn directly
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start with custom script
bash scripts/dev.sh
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_llms.py

# Run specific test function
uv run pytest tests/unit/test_llms.py::test_llm_factory_groq

# Run with verbose output
uv run pytest -v

# Run tests matching pattern
uv run pytest -k "test_llm"
```

### Code Quality
```bash
# Format all code
uv run black src/ tests/

# Check formatting without changes
uv run black --check src/ tests/

# Lint with Ruff
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Type checking with MyPy
uv run mypy src/

# Run all quality checks
bash scripts/lint.sh
```

### Package Management
```bash
# Add a new package
uv add requests

# Add a dev dependency
uv add --dev ipython

# Remove a package
uv remove requests

# Update dependencies
uv sync

# Show installed packages
uv pip list

# Generate requirements.txt (if needed)
uv pip freeze > requirements.txt
```

### API Testing

#### Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Simple chat
curl -X POST http://localhost:8000/api/v1/chat/simple \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'

# Chat with web search
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the latest AI developments?"}'

# Research agent
curl -X POST http://localhost:8000/api/v1/research/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Quantum computing trends", "max_results": 5}'

# Content writer
curl -X POST http://localhost:8000/api/v1/writer/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "Future of AI", "content_type": "blog", "tone": "professional"}'
```

#### Using httpie (if installed)
```bash
# Install httpie
pip install httpie

# Simple chat
http POST :8000/api/v1/chat/simple message="Hello!"

# Research
http POST :8000/api/v1/research/ query="AI trends" max_results=5
```

#### Using Python
```python
import requests

# Simple chat
response = requests.post(
    "http://localhost:8000/api/v1/chat/simple",
    json={"message": "Hello!"}
)
print(response.json())

# Research
response = requests.post(
    "http://localhost:8000/api/v1/research/",
    json={"query": "AI trends", "max_results": 5}
)
print(response.json())
```

### Logs
```bash
# View real-time logs
tail -f logs/app_*.log

# View error logs
tail -f logs/error_*.log

# Search logs
grep "ERROR" logs/app_*.log

# View last 100 lines
tail -n 100 logs/app_*.log
```

### Git Operations
```bash
# Initial commit (if not done)
git add .
git commit -m "Initial commit: Production-ready Agentic AI platform"

# Create feature branch
git checkout -b feature/new-agent

# Commit changes
git add .
git commit -m "Add new agent type"

# Push to remote
git push origin feature/new-agent
```

### Environment Variables
```bash
# View current environment
cat .env

# Edit environment
nano .env

# Required variables:
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# Optional variables:
OPENAI_API_KEY=your_key_here
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
```

### Debugging
```bash
# Run with debug mode
DEBUG=true uv run python main.py

# Python interactive mode
uv run python
>>> from src.llms.base import LLMFactory
>>> llm = LLMFactory.create("groq")
>>> print(llm)

# IPython for better debugging (install first: uv add --dev ipython)
uv run ipython
```

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=production
export DEBUG=false
export RELOAD=false

# Run with multiple workers
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn (install: uv add gunicorn)
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Documentation
```bash
# Generate API docs (already available at /docs)
# Access: http://localhost:8000/docs

# View ReDoc
# Access: http://localhost:8000/redoc

# Read local docs
cat README.md
cat PROJECT_SUMMARY.md
cat docs/ARCHITECTURE.md
cat docs/QUICKSTART.md
```

## Common Workflows

### Adding a New Agent
```bash
# 1. Create state schema
nano src/agents/states/custom.py

# 2. Create node functions
nano src/agents/nodes/custom.py

# 3. Create graph builder
nano src/agents/graphs/custom.py

# 4. Register in factory (edit src/agents/graphs/base.py)

# 5. Create API endpoint
nano src/api/v1/custom.py

# 6. Add to main.py router
nano main.py

# 7. Test
uv run pytest tests/unit/test_custom.py
```

### Adding a New LLM Provider
```bash
# 1. Implement LLM class
nano src/llms/custom.py

# 2. Register in factory (edit src/llms/base.py)

# 3. Add configuration (edit src/core/config.py)

# 4. Test
uv run pytest tests/unit/test_llms.py
```

### Adding a New Tool
```bash
# 1. Create tool function
nano src/tools/custom.py

# 2. Register in tools/base.py

# 3. Add to available tools list

# 4. Test with agent
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in .env
PORT=8001
```

### Import Errors
```bash
# Reinstall dependencies
uv sync

# Check Python path
uv run python -c "import sys; print(sys.path)"

# Clear cache
rm -rf __pycache__ src/__pycache__
find . -type d -name __pycache__ -exec rm -rf {} +
```

### API Key Errors
```bash
# Verify .env file exists
ls -la .env

# Check API keys are set
grep API_KEY .env

# Test API key (Groq example)
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

### Database Issues
```bash
# Reset database (if using)
rm data/app.db

# Run migrations (if implemented)
# alembic upgrade head
```

## Useful Shortcuts

### Aliases (add to ~/.bashrc or ~/.zshrc)
```bash
alias uv-run="uv run"
alias uv-test="uv run pytest"
alias uv-format="uv run black src/ tests/"
alias uv-lint="uv run ruff check src/ tests/"
alias uv-serve="uv run python main.py"
```

### VS Code Tasks (add to .vscode/tasks.json)
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Server",
      "type": "shell",
      "command": "uv run python main.py",
      "problemMatcher": []
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "uv run pytest",
      "problemMatcher": []
    }
  ]
}
```

## Performance Tips

1. **Enable LangSmith tracing** for debugging: `LANGCHAIN_TRACING_V2=true`
2. **Use caching** for repeated queries
3. **Adjust rate limits** in `.env`
4. **Monitor logs** in `logs/` directory
5. **Profile slow endpoints** with `cProfile`

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Never commit `.env` file
- [ ] Use strong API keys
- [ ] Enable rate limiting in production
- [ ] Configure CORS properly
- [ ] Use HTTPS in production
- [ ] Regular dependency updates: `uv sync`
- [ ] Review logs for suspicious activity

---

**Pro Tip**: Bookmark this file for quick reference! 📖

**Questions?** Check:
- README.md for overview
- PROJECT_SUMMARY.md for details
- docs/QUICKSTART.md for tutorials
- docs/ARCHITECTURE.md for technical deep dive
