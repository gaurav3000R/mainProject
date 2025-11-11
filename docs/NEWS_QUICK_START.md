# News Summarization Quick Start

## 🚀 Quick Test

### 1. Start the Server
```bash
python main.py
# or
uvicorn main:app --reload
```

### 2. Test the Endpoint

**Simple Request:**
```bash
curl -X POST http://localhost:8000/api/v1/news/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence news today",
    "max_results": 5
  }'
```

**Detailed Request (with full articles):**
```bash
curl -X POST http://localhost:8000/api/v1/news/summarize/detailed \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space exploration 2024",
    "max_results": 10
  }'
```

### 3. Check Results

View saved summaries:
```bash
ls -lh data/news_summaries/
cat data/news_summaries/latest_file.json | jq .
```

## 📡 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/news/summarize` | POST | Simple news summary |
| `/api/v1/news/summarize/detailed` | POST | Detailed with articles |
| `/api/v1/news/health` | GET | Health check |

## 🔄 Workflow Steps

1. **Fetch News** - Retrieves articles via web search API
2. **Summarize** - AI generates comprehensive summary
3. **Save Result** - Stores to `data/news_summaries/`

## 📊 Example Response

```json
{
  "success": true,
  "query": "AI news",
  "articles_count": 5,
  "summary": "Recent developments in AI include...",
  "saved_path": "data/news_summaries/20251111_050000_AI_news.json",
  "status": "completed"
}
```

## 🧪 Test Script

Run the standalone test:
```bash
python examples/test_news_summary.py
```

## 📖 Documentation

Full documentation: [docs/NEWS_SUMMARIZATION.md](../docs/NEWS_SUMMARIZATION.md)

## 🎯 Use Cases

- Daily news briefings
- Research topic monitoring
- Competitive intelligence
- Content curation
- Market trend analysis
- Event tracking

## ⚙️ Configuration

Adjust settings in the request:
```json
{
  "query": "your search query",
  "max_results": 10  // 1-20 articles
}
```

## 🔗 Integration

Use in your code:
```python
from src.agents.graphs.news import NewsSummarizationGraph
from src.llms.base import LLMFactory

llm = LLMFactory.create("groq")
graph = NewsSummarizationGraph(llm)
result = await graph.arun("tech news", max_results=5)
print(result["summary"])
```

## 🐛 Troubleshooting

**Issue:** No articles found
- Check your internet connection
- Try a different query
- Verify TAVILY_API_KEY is set

**Issue:** Summarization fails
- Check GROQ_API_KEY or OPENAI_API_KEY
- Verify LLM provider is available

**Issue:** Save fails
- Check write permissions on `data/` directory
- Ensure disk space available
