# News Summarization Workflow

## Overview

A LangGraph workflow that fetches news articles, summarizes them using AI, and saves the results.

**Workflow:** Start → Fetch News (API) → Summarize → Save Result → End

## Architecture

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌──────────────┐
│ Fetch News   │ ← Web Search API
│  (Node 1)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Summarize    │ ← LLM (Groq/OpenAI)
│  (Node 2)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Save Result  │ → data/news_summaries/
│  (Node 3)    │
└──────┬───────┘
       │
       ▼
   ┌─────┐
   │ End │
   └─────┘
```

## API Endpoints

### 1. Summarize News (Simple)

```bash
POST /api/v1/news/summarize
```

**Request:**
```json
{
  "query": "artificial intelligence news today",
  "max_results": 5
}
```

**Response:**
```json
{
  "success": true,
  "query": "artificial intelligence news today",
  "articles_count": 5,
  "summary": "AI technology continues to advance...",
  "saved_path": "data/news_summaries/20251111_050000_artificial_intelligence.json",
  "status": "completed",
  "error": null
}
```

### 2. Summarize News (Detailed)

```bash
POST /api/v1/news/summarize/detailed
```

**Request:**
```json
{
  "query": "climate change 2024",
  "max_results": 10
}
```

**Response:**
```json
{
  "success": true,
  "query": "climate change 2024",
  "articles": [
    {
      "title": "Climate Summit 2024 Outcomes",
      "content": "World leaders gathered...",
      "url": "https://example.com/article",
      "source": "web"
    }
  ],
  "summary": "Climate change discussions in 2024...",
  "saved_path": "data/news_summaries/20251111_050100_climate_change.json",
  "status": "completed",
  "error": null
}
```

### 3. Health Check

```bash
GET /api/v1/news/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "news_summarization",
  "workflow": "Start → Fetch News → Summarize → Save → End"
}
```

## Usage Examples

### cURL Example

```bash
# Simple summarization
curl -X POST http://localhost:8000/api/v1/news/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "query": "technology trends 2024",
    "max_results": 5
  }'

# Detailed with articles
curl -X POST http://localhost:8000/api/v1/news/summarize/detailed \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space exploration news",
    "max_results": 8
  }'
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Fetch and summarize news
response = requests.post(
    f"{BASE_URL}/news/summarize",
    json={
        "query": "AI breakthroughs 2024",
        "max_results": 5
    }
)

result = response.json()
print(f"Summary: {result['summary']}")
print(f"Articles: {result['articles_count']}")
print(f"Saved to: {result['saved_path']}")
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/api/v1/news/summarize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'quantum computing news',
    max_results: 5
  })
});

const result = await response.json();
console.log('Summary:', result.summary);
console.log('Saved to:', result.saved_path);
```

## Workflow Components

### State (`src/agents/states/news.py`)

```python
class NewsSummaryState(TypedDict):
    query: str              # Input: search query
    max_results: int        # Input: max articles
    news_articles: List     # Intermediate: fetched articles
    summary: str            # Output: AI summary
    saved_path: str         # Output: saved file path
    error: str              # Error message if any
    status: str             # Current workflow status
```

### Nodes (`src/agents/nodes/news.py`)

1. **fetch_news_node**: Fetches news articles using web search
2. **summarize_news_node**: Uses LLM to generate summary
3. **save_result_node**: Saves results to JSON file

### Graph (`src/agents/graphs/news.py`)

```python
class NewsSummarizationGraph:
    def run(query: str, max_results: int = 5) -> NewsSummaryState:
        """Run the workflow synchronously"""
        
    async def arun(query: str, max_results: int = 5) -> NewsSummaryState:
        """Run the workflow asynchronously"""
```

## Output Format

Results are saved to `data/news_summaries/` with the following structure:

```json
{
  "query": "AI news",
  "timestamp": "20251111_050000",
  "articles_count": 5,
  "articles": [
    {
      "title": "Article Title",
      "content": "Article content...",
      "url": "https://...",
      "source": "web"
    }
  ],
  "summary": "Comprehensive AI-generated summary...",
  "status": "completed"
}
```

## Configuration

### Adjust Max Results

```python
# In request
{
  "query": "news query",
  "max_results": 10  # Default: 5, Max: 20
}
```

### Customize Summarization

Edit the prompt in `src/agents/nodes/news.py`:

```python
prompt = f"""You are a news summarizer...
[Customize this prompt to change summary style]
"""
```

## Error Handling

All errors are captured and returned in the response:

```json
{
  "success": false,
  "error": "Failed to fetch news: API timeout",
  "status": "error"
}
```

## Testing

```bash
# Health check
curl http://localhost:8000/api/v1/news/health

# Test summarization
curl -X POST http://localhost:8000/api/v1/news/summarize \
  -H "Content-Type: application/json" \
  -d '{"query": "test news", "max_results": 3}'
```

## Integration with Other Services

### Use in Chat Agent

```python
from src.agents.graphs.news import NewsSummarizationGraph

# In your chat agent
graph = NewsSummarizationGraph(llm)
result = await graph.arun("latest AI news")
summary = result["summary"]
```

### Scheduled Tasks

```python
import asyncio
from src.agents.graphs.news import NewsSummarizationGraph
from src.llms.base import LLMFactory

async def daily_news_summary():
    """Run daily news summary"""
    llm = LLMFactory.create("groq")
    graph = NewsSummarizationGraph(llm)
    
    topics = ["AI", "Technology", "Science"]
    for topic in topics:
        result = await graph.arun(f"{topic} news today")
        print(f"Saved {topic} summary to {result['saved_path']}")

# Schedule with cron or celery
asyncio.run(daily_news_summary())
```

## Files Created

```
src/
├── agents/
│   ├── states/
│   │   └── news.py          # Workflow state definition
│   ├── nodes/
│   │   └── news.py          # Workflow nodes
│   └── graphs/
│       └── news.py          # Workflow graph
└── api/
    └── v1/
        └── news.py          # API endpoints

data/
└── news_summaries/          # Saved results
```

## Performance

- **Average execution time**: 5-15 seconds
- **Concurrent requests**: Supported (async)
- **Rate limiting**: Respects global rate limits

## Future Enhancements

- [ ] Add RSS feed support
- [ ] Multi-language summarization
- [ ] Sentiment analysis
- [ ] Trend detection
- [ ] Email notifications
- [ ] PDF export
- [ ] Webhook integration
- [ ] Caching layer

## Related Documentation

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [API Reference](../README.md)
- [Conversation Memory](./CONVERSATION_MEMORY.md)
