#!/usr/bin/env python3
"""
LangSmith Annotation Examples
Demonstrates all methods from: https://docs.langchain.com/langsmith/annotate-code

This shows:
1. Automatic tracing (via LANGCHAIN_TRACING_V2)
2. @traceable decorator
3. RunTree for manual tracing
4. trace() context manager
"""

import os
from typing import Dict, Any
from langsmith import traceable, trace
from langsmith.run_trees import RunTree
from langchain_core.messages import HumanMessage
from src.core.config import setup_langsmith
from src.agents.graphs.deployable import chatbot_graph
from src.utils.logger import app_logger


# ============================================================================
# METHOD 1: Automatic Tracing (Current Implementation)
# ============================================================================
# This is already working - all LangChain/LangGraph calls are auto-traced
# when LANGCHAIN_TRACING_V2=true

def example_automatic_tracing():
    """
    Automatic tracing - no code changes needed.
    All LangChain/LangGraph operations are automatically traced.
    """
    print("\n" + "="*70)
    print("METHOD 1: Automatic Tracing (Current Setup)")
    print("="*70)
    print("✅ Already enabled via LANGCHAIN_TRACING_V2=true")
    print("   All graph executions are automatically traced")
    
    # Just use the graph normally
    graph = chatbot_graph()
    state = {"messages": [HumanMessage(content="Test automatic tracing")]}
    result = graph.invoke(state)
    
    print("✓ Graph executed - check LangSmith for automatic trace")


# ============================================================================
# METHOD 2: @traceable Decorator
# ============================================================================
# Best for: Custom functions you want to trace

@traceable(name="custom_data_processor", run_type="chain")
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Custom function with @traceable decorator.
    Automatically creates a trace with inputs, outputs, and timing.
    """
    # Your business logic here
    processed = {
        "original": data,
        "processed": True,
        "count": len(data)
    }
    return processed


@traceable(name="llm_call_wrapper", run_type="llm")
def call_llm_with_trace(prompt: str) -> str:
    """Example of tracing a custom LLM call."""
    from src.llms.base import LLMFactory
    from src.core.config import settings
    
    llm = LLMFactory.create(
        provider=settings.default_llm_provider,
        model_name=settings.default_model
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content if hasattr(response, 'content') else str(response)


def example_traceable_decorator():
    """Demonstrate @traceable decorator."""
    print("\n" + "="*70)
    print("METHOD 2: @traceable Decorator")
    print("="*70)
    
    # Call traced function
    result1 = process_data({"key": "value", "number": 42})
    print(f"✓ Traced function executed: {result1}")
    
    # Call traced LLM wrapper
    result2 = call_llm_with_trace("What is 2+2?")
    print(f"✓ Traced LLM call: {result2[:50]}...")
    
    print("✓ Check LangSmith for traces named 'custom_data_processor' and 'llm_call_wrapper'")


# ============================================================================
# METHOD 3: RunTree (Manual Tracing)
# ============================================================================
# Best for: Fine-grained control, complex workflows, custom metadata

def example_runtree():
    """Demonstrate RunTree for manual tracing."""
    print("\n" + "="*70)
    print("METHOD 3: RunTree (Manual Control)")
    print("="*70)
    
    # Create a parent run
    parent_run = RunTree(
        name="Custom Workflow",
        run_type="chain",
        inputs={"task": "Process user request"},
        extra={"user_id": "123", "session": "abc"},
        tags=["manual", "custom"]
    )
    parent_run.post()  # Start the trace
    
    try:
        # Create child runs
        step1 = parent_run.create_child(
            name="Step 1: Validate Input",
            run_type="tool",
            inputs={"input": "user query"}
        )
        step1.post()
        # ... do work ...
        step1.end(outputs={"valid": True})
        step1.patch()
        
        step2 = parent_run.create_child(
            name="Step 2: Process",
            run_type="chain",
            inputs={"validated_input": "user query"}
        )
        step2.post()
        # ... do work ...
        step2.end(outputs={"result": "processed data"})
        step2.patch()
        
        # End parent
        parent_run.end(outputs={"status": "complete", "result": "success"})
        parent_run.patch()
        
        print("✓ Manual trace created with nested runs")
        print("✓ Check LangSmith for 'Custom Workflow' trace")
        
    except Exception as e:
        parent_run.end(error=str(e))
        parent_run.patch()
        raise


# ============================================================================
# METHOD 4: trace() Context Manager
# ============================================================================
# Best for: Tracing code blocks, temporary tracing

def example_trace_context():
    """Demonstrate trace() context manager."""
    print("\n" + "="*70)
    print("METHOD 4: trace() Context Manager")
    print("="*70)
    
    # Trace a code block
    with trace(
        name="Data Processing Pipeline",
        run_type="chain",
        inputs={"data": [1, 2, 3, 4, 5]},
        tags=["pipeline", "processing"]
    ) as run:
        # Your code here
        data = [1, 2, 3, 4, 5]
        
        # Nested trace
        with trace(
            name="Transform Data",
            run_type="tool",
            inputs={"data": data}
        ):
            transformed = [x * 2 for x in data]
        
        # Another nested trace
        with trace(
            name="Aggregate Results",
            run_type="tool",
            inputs={"data": transformed}
        ):
            result = sum(transformed)
        
        # Set outputs on parent
        run.end(outputs={"result": result})
    
    print(f"✓ Context manager trace completed: result={result}")
    print("✓ Check LangSmith for 'Data Processing Pipeline' trace")


# ============================================================================
# METHOD 5: Hybrid - Combining Methods
# ============================================================================

@traceable(name="hybrid_workflow", run_type="chain")
def hybrid_example(input_data: str):
    """
    Combine automatic tracing with manual annotations.
    Best practice for complex applications.
    """
    # This function is automatically traced via @traceable
    
    # Use context manager for specific sections
    with trace(name="preprocessing", run_type="tool"):
        cleaned = input_data.strip().lower()
    
    # Call other traced functions
    processed = process_data({"input": cleaned})
    
    # Use RunTree for custom metadata
    analysis_run = RunTree(
        name="Analysis Step",
        run_type="tool",
        inputs={"data": processed},
        tags=["analysis", "hybrid"]
    )
    analysis_run.post()
    
    # Do analysis
    result = {"analyzed": True, "data": processed}
    
    analysis_run.end(outputs=result)
    analysis_run.patch()
    
    return result


def example_hybrid():
    """Demonstrate hybrid approach."""
    print("\n" + "="*70)
    print("METHOD 5: Hybrid Approach (Recommended)")
    print("="*70)
    
    result = hybrid_example("  TEST DATA  ")
    print(f"✓ Hybrid workflow executed: {result}")
    print("✓ Check LangSmith for nested traces showing all annotation methods")


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    """Run all annotation examples."""
    # Setup LangSmith
    setup_langsmith()
    
    print("="*70)
    print("LANGSMITH ANNOTATION METHODS DEMO")
    print("="*70)
    print(f"Dashboard: https://api.smith.langchain.com/projects/p/{os.getenv('LANGCHAIN_PROJECT')}")
    
    try:
        # Run examples
        example_automatic_tracing()
        example_traceable_decorator()
        example_runtree()
        example_trace_context()
        example_hybrid()
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*70)
        print("\nCheck your LangSmith dashboard to see:")
        print("  1. Automatic graph traces")
        print("  2. @traceable decorated functions")
        print("  3. Manual RunTree traces")
        print("  4. trace() context manager traces")
        print("  5. Hybrid combined traces")
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
