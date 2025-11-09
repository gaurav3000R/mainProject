# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Setup Project
```bash
cd mainProject
uv sync
cp .env.example .env
```

### Step 3: Add API Keys to `.env`
```bash
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your keys:
- Groq: https://console.groq.com/keys
- Tavily: https://app.tavily.com/

### Step 4: Run Server
```bash
uv run python main.py
```

### Step 5: Test API
Open http://localhost:8000/docs

## 📝 First API Call

### Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/chat/simple" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat/simple",
    json={"message": "Hello, how are you?"}
)
print(response.json())
```

### Using JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:8000/api/v1/chat/simple', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Hello, how are you?'})
});
const data = await response.json();
console.log(data);
```

## 🎯 Common Tasks

### Run Tests
```bash
uv run pytest
```

### Format Code
```bash
uv run black src/ tests/
```

### Check Code Quality
```bash
uv run ruff check src/
```

### Add New Dependency
```bash
uv add package-name
```

## 🔧 Troubleshooting

### "Module not found" Error
```bash
uv sync
```

### Port Already in Use
Edit `.env` and change `PORT=8000` to another port.

### API Key Error
Make sure your `.env` file has valid API keys.

## 📚 Next Steps

1. Read [Architecture](ARCHITECTURE.md) to understand the system
2. Check [API Examples](../README.md#-api-examples) for more use cases
3. Explore `src/` to understand the code structure
4. Write your first custom agent!

## 💡 Pro Tips

- Use `uv run uvicorn main:app --reload` for auto-reload during development
- Check logs in `logs/` directory for debugging
- Use `/docs` endpoint for interactive API testing
- Enable LangSmith tracing by setting `LANGCHAIN_TRACING_V2=true`

## 🆘 Need Help?

- Check the main [README](../README.md)
- Review test files for usage examples
- Open an issue on GitHub

Happy coding! 🎉
