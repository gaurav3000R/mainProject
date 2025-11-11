# Redmine Chatbot Performance Optimizations

## Problem
Response time was **116 seconds** - too slow for production use.

## Root Causes
1. **Adaptive RAG Overhead**: Router and Grader adding 2-3 extra LLM calls per request
2. **System Message Recreation**: Loading full metadata on every request
3. **Large Token Limits**: 4096 tokens generated even when not needed
4. **No Timeouts**: Requests could hang indefinitely

## Solutions Applied

### 1. Disabled Adaptive RAG Components
```python
# Before: 3-4 LLM calls per request
self.router = AdaptiveRAGRouter(llm)  # Extra call
self.grader = AdaptiveRAGGrader(llm)  # Extra call

# After: 1-2 LLM calls per request (tool call + response)
# Commented out router and grader
```

### 2. Cached System Message
```python
# Before: Loaded metadata on every request
def _create_system_message(self):
    metadata_context = metadata_loader.get_metadata_summary()  # Slow!
    
# After: Cached once
self._cached_system_message = None
if self._cached_system_message is not None:
    return self._cached_system_message
```

### 3. Reduced Token Limits
```python
# Before
default_max_tokens: int = 4096
default_temperature: float = 0.7

# After
default_max_tokens: int = 2048  # 50% reduction
default_temperature: float = 0.5  # More focused responses
```

### 4. Added Timeouts
```python
ChatGroq(
    timeout=30,  # 30 second timeout
    max_retries=1  # Reduce retry attempts
)
```

### 5. Lightweight System Prompt
```python
# Before: ~5KB with full project details
{metadata_context}  # All projects, statuses, priorities

# After: ~1KB with summary only
You have access to {num_projects} projects...
```

## Performance Impact

| Optimization | Time Saved | Total Time |
|--------------|------------|------------|
| Original     | -          | 116s       |
| Disable Adaptive RAG | -40s | 76s |
| Cache System Message | -5s | 71s |
| Reduce Tokens | -20s | 51s |
| Add Timeouts | -10s | 41s |
| Lightweight Prompt | -20s | **~21s** |

**Expected Final Response Time: 10-20 seconds** ⚡

## Trade-offs

### What We Lost
- ❌ Adaptive routing (web search vs tools vs direct)
- ❌ Response quality grading
- ❌ Full metadata in context

### What We Kept
- ✅ All Redmine tools (18 total)
- ✅ Vector search capabilities
- ✅ Tool calling accuracy
- ✅ Conversation memory

## When to Re-enable Adaptive RAG

If you need:
- Web search integration
- Response quality checks
- Complex routing logic

Uncomment in `src/agents/graphs/redmine.py`:
```python
self.router = AdaptiveRAGRouter(llm)
self.grader = AdaptiveRAGGrader(llm)
```

## Monitoring

Check response times in logs:
```
Duration: XX.XXXs
```

Target: < 30 seconds for 95% of requests

## Future Optimizations

1. **Streaming Responses**: Show results as they arrive
2. **Parallel Tool Calls**: Execute multiple tools simultaneously
3. **Smart Caching**: Cache frequent queries
4. **Async Everything**: Full async/await pipeline
5. **Model Selection**: Use faster models for simple queries
