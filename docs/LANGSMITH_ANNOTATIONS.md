# LangSmith Code Annotation - Complete Guide

Based on: https://docs.langchain.com/langsmith/annotate-code

## Overview

Your project already uses **automatic tracing** via environment variables. This document shows you 4 additional annotation methods for more control.

## Current Implementation: ✅ WORKING

Your setup uses **Method 1: Automatic Tracing**

```python
# .env file
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=agentic-ai-platform
```

**All LangChain/LangGraph operations are automatically traced** - no code changes needed!

## 5 Annotation Methods

### 1. Automatic Tracing ✅ (Current)

**When to use:** Always enabled for LangChain/LangGraph

**How it works:**
- Set `LANGCHAIN_TRACING_V2=true` in `.env`
- All LangChain/LangGraph calls auto-traced
- Zero code changes required

**Example:**
```python
from src.agents.graphs.deployable import chatbot_graph

graph = chatbot_graph()
result = graph.invoke(state)  # Automatically traced!
```

**Status:** ✅ Already working in your project

---

### 2. @traceable Decorator

**When to use:** Custom functions you want to trace

**Pros:**
- Clean, declarative syntax
- Automatic input/output logging
- Minimal code changes

**Example:**
```python
from langsmith import traceable

@traceable(name="process_user_input", run_type="chain")
def process_input(user_data: dict) -> dict:
    # Your business logic
    cleaned = user_data.get("text", "").strip()
    return {"processed": cleaned, "length": len(cleaned)}

# Automatically traced when called
result = process_input({"text": "  hello  "})
```

**Run types:**
- `"chain"` - Sequential operations
- `"tool"` - Tool/function calls
- `"llm"` - LLM interactions
- `"retriever"` - Vector DB queries
- `"embedding"` - Embedding generation

---

### 3. RunTree (Manual Control)

**When to use:** 
- Complex workflows with multiple steps
- Need custom metadata
- Parent/child relationships
- Error handling

**Pros:**
- Fine-grained control
- Custom metadata
- Nested runs
- Explicit error handling

**Example:**
```python
from langsmith.run_trees import RunTree

# Create parent run
workflow = RunTree(
    name="User Onboarding",
    run_type="chain",
    inputs={"user_id": "123", "email": "user@example.com"},
    tags=["onboarding", "production"],
    extra={"version": "2.0", "region": "us-east"}
)
workflow.post()  # Start tracing

try:
    # Step 1
    validation = workflow.create_child(
        name="Validate User Data",
        run_type="tool",
        inputs={"email": "user@example.com"}
    )
    validation.post()
    # ... validation logic ...
    validation.end(outputs={"valid": True})
    validation.patch()
    
    # Step 2
    processing = workflow.create_child(
        name="Create Account",
        run_type="chain",
        inputs={"user_id": "123"}
    )
    processing.post()
    # ... account creation ...
    processing.end(outputs={"account_id": "acc_456"})
    processing.patch()
    
    # Complete workflow
    workflow.end(outputs={"success": True, "account_id": "acc_456"})
    workflow.patch()
    
except Exception as e:
    workflow.end(error=str(e))
    workflow.patch()
    raise
```

---

### 4. trace() Context Manager

**When to use:**
- Trace specific code blocks
- Temporary/conditional tracing
- Quick debugging

**Pros:**
- Pythonic syntax
- Easy to add/remove
- Scoped tracing

**Example:**
```python
from langsmith import trace

def process_order(order_data):
    # Trace the entire function
    with trace(
        name="Process Order",
        run_type="chain",
        inputs={"order_id": order_data["id"]},
        tags=["orders", "processing"]
    ) as run:
        
        # Nested trace for validation
        with trace(name="Validate Order", run_type="tool"):
            validate(order_data)
        
        # Nested trace for payment
        with trace(name="Process Payment", run_type="tool"):
            payment_result = charge_card(order_data)
        
        # Nested trace for fulfillment
        with trace(name="Schedule Fulfillment", run_type="chain"):
            fulfillment = schedule_shipment(order_data)
        
        # Set final outputs
        result = {"status": "complete", "fulfillment_id": fulfillment.id}
        run.end(outputs=result)
        return result
```

---

### 5. Hybrid Approach (Recommended)

**Best practice:** Combine multiple methods

```python
from langsmith import traceable, trace
from langsmith.run_trees import RunTree

@traceable(name="main_workflow", run_type="chain")
def process_complex_request(request_data):
    """
    Main workflow - automatically traced via decorator
    """
    
    # Use context manager for specific sections
    with trace(name="data_validation", run_type="tool"):
        validated = validate_and_clean(request_data)
    
    # Use RunTree for complex sub-workflow with custom metadata
    analysis = RunTree(
        name="Deep Analysis",
        run_type="chain",
        inputs={"data": validated},
        tags=["analysis", "ml"],
        extra={"model_version": "3.2", "confidence_threshold": 0.85}
    )
    analysis.post()
    
    try:
        # Your ML/AI processing here
        result = run_ml_model(validated)
        analysis.end(outputs=result)
    finally:
        analysis.patch()
    
    # Call other traced functions
    final = format_results(result)  # Also @traceable
    
    return final
```

## Implementation in Your Project

### Files Created

1. **`src/agents/nodes/traced_nodes.py`**
   - Example nodes with @traceable decorators
   - Drop-in replacements for base nodes

2. **`examples/langsmith_annotations.py`**
   - Comprehensive examples of all 5 methods
   - Run: `python examples/langsmith_annotations.py`

3. **`src/utils/traced_executor.py`**
   - Enhanced graph executor with custom tracing
   - Convenience functions for common patterns

### Quick Start

**Test the decorator:**
```bash
python -c "from langsmith import traceable; @traceable(name='test'); def f(x): return x*2; print(f(5))"
```

**Run all examples:**
```bash
python examples/langsmith_annotations.py
```

**Use in your code:**
```python
# Option 1: Keep using automatic tracing (no changes)
from src.agents.graphs.deployable import chatbot_graph
graph = chatbot_graph()
result = graph.invoke(state)

# Option 2: Add @traceable to custom functions
from langsmith import traceable

@traceable(name="my_custom_logic")
def my_function(data):
    return process(data)

# Option 3: Use enhanced executor
from src.utils.traced_executor import TracedGraphExecutor

result = TracedGraphExecutor.execute(
    "chatbot",
    state,
    run_name="user_123_chat",
    tags=["production"],
    metadata={"user_id": "123"}
)
```

## Comparison Table

| Method | Code Changes | Control | Best For |
|--------|--------------|---------|----------|
| Automatic | None | Low | LangChain/LangGraph (✅ current) |
| @traceable | Minimal | Medium | Custom functions |
| RunTree | More | High | Complex workflows |
| trace() | Minimal | Medium | Code blocks |
| Hybrid | Varies | High | Production apps (recommended) |

## Best Practices

### 1. Start with Automatic Tracing
✅ You're already doing this! No changes needed.

### 2. Add @traceable for Business Logic
```python
@traceable(name="calculate_pricing", run_type="chain")
def calculate_price(items, discounts):
    # Your pricing logic
    pass
```

### 3. Use RunTree for Complex Flows
When you have multi-step processes with branches and error handling.

### 4. Add Metadata
```python
@traceable(
    name="api_call",
    run_type="tool",
    tags=["external_api", "third_party"],
    metadata={"version": "2.0", "timeout": 30}
)
def call_external_api(endpoint, data):
    pass
```

### 5. Organize with Tags
```python
# Development
tags=["dev", "testing", "experiment"]

# Production
tags=["prod", "user_facing", "critical"]

# Feature-based
tags=["authentication", "payment", "notification"]
```

## Dashboard Views

After adding annotations, your LangSmith dashboard will show:

1. **Hierarchy:** Parent/child relationships
2. **Timing:** Duration for each annotated section
3. **Metadata:** Custom tags and extra data
4. **Filtering:** Filter by run_type, tags, etc.
5. **Search:** Find traces by name

## Troubleshooting

### Traces not appearing with @traceable

**Check:**
```python
import os
print(os.getenv('LANGCHAIN_TRACING_V2'))  # Should be 'true'
print(os.getenv('LANGCHAIN_API_KEY'))     # Should be set
```

**Solution:** Ensure environment is set before importing:
```python
from src.core.config import setup_langsmith
setup_langsmith()  # Sets environment variables

# Now import and use @traceable
from langsmith import traceable
```

### RunTree not showing in dashboard

**Issue:** Forgot to call `.post()` or `.patch()`

**Solution:**
```python
run = RunTree(...)
run.post()      # ← Required to start
# ... do work ...
run.end(...)
run.patch()     # ← Required to finish
```

## Summary

✅ **Your project is already tracing!** - Automatic tracing is enabled

📚 **4 additional methods available** - For more control when needed

🎯 **Recommended approach:**
1. Keep automatic tracing (no changes)
2. Add `@traceable` to important custom functions
3. Use `RunTree` for complex multi-step workflows
4. Add tags and metadata for better organization

🔗 **Resources:**
- LangSmith Docs: https://docs.smith.langchain.com/
- Your Dashboard: https://api.smith.langchain.com/projects/p/agentic-ai-platform
- Examples: `python examples/langsmith_annotations.py`
