#!/bin/bash
# Quick graph testing script
# Usage: ./test_graph.sh [graph_name]

cd "$(dirname "$0")"

echo "════════════════════════════════════════════════════════════════"
echo "🧪 LANGGRAPH QUICK TESTER"
echo "════════════════════════════════════════════════════════════════"
echo ""

if [ -z "$1" ]; then
    echo "Available graphs to test:"
    echo "  1. chatbot"
    echo "  2. chatbot_with_tools"
    echo "  3. research"
    echo "  4. writer"
    echo "  5. news"
    echo "  6. redmine"
    echo "  7. all"
    echo ""
    echo "Usage: ./test_graph.sh <graph_name>"
    echo "Example: ./test_graph.sh chatbot"
    exit 0
fi

GRAPH=$1

case $GRAPH in
    chatbot)
        echo "Testing: CHATBOT"
        python -c "
from langchain_core.messages import HumanMessage
from src.agents.graphs.deployable import chatbot_graph

graph = chatbot_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')

state = {'messages': [HumanMessage(content='Hello!')]}
result = graph.invoke(state)
print(f'✓ Response: {result[\"messages\"][-1].content[:100]}...')
print('✅ CHATBOT WORKING')
"
        ;;
    
    chatbot_with_tools)
        echo "Testing: CHATBOT WITH TOOLS"
        python -c "
from langchain_core.messages import HumanMessage
from src.agents.graphs.deployable import chatbot_with_tools_graph

graph = chatbot_with_tools_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')

state = {'messages': [HumanMessage(content='What is 2+2?')]}
result = graph.invoke(state)
print(f'✓ Response: {result[\"messages\"][-1].content[:100]}...')
print('✅ CHATBOT WITH TOOLS WORKING')
"
        ;;
    
    research)
        echo "Testing: RESEARCH AGENT"
        python -c "
from src.agents.graphs.deployable import research_graph

graph = research_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')
print('✅ RESEARCH AGENT STRUCTURE OK')
print('  Note: Full test requires web search API key')
"
        ;;
    
    writer)
        echo "Testing: CONTENT WRITER"
        python -c "
from src.agents.graphs.deployable import writer_graph

graph = writer_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')
print('✅ CONTENT WRITER STRUCTURE OK')
print('  Note: Full test takes 30-60 seconds for outline→draft→polish')
"
        ;;
    
    news)
        echo "Testing: NEWS SUMMARIZATION"
        python -c "
from src.agents.graphs.deployable import news_graph

graph = news_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')
print('✅ NEWS SUMMARIZATION STRUCTURE OK')
print('  Note: Full test requires news API access')
"
        ;;
    
    redmine)
        echo "Testing: REDMINE CHATBOT"
        python -c "
from src.agents.graphs.deployable import redmine_graph

graph = redmine_graph()
print('✓ Graph compiled')
print(f'  Nodes: {list(graph.nodes.keys())}')
print('✅ REDMINE CHATBOT STRUCTURE OK')
print('  Note: Full test requires Redmine API configuration')
"
        ;;
    
    all)
        echo "Testing all graphs..."
        echo ""
        for g in chatbot chatbot_with_tools research writer news redmine; do
            ./test_graph.sh $g
            echo ""
        done
        ;;
    
    *)
        echo "❌ Unknown graph: $GRAPH"
        echo "Available: chatbot, chatbot_with_tools, research, writer, news, redmine, all"
        exit 1
        ;;
esac
