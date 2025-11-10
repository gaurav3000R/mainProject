#!/bin/bash
# Quick start script for LangGraph Studio

echo "🚀 Starting LangGraph Development Server..."
echo ""
echo "📊 Available Graphs:"
echo "  - chatbot: Simple conversational bot"
echo "  - chatbot_with_tools: Chat with web search"
echo "  - research_agent: Research and summarization"
echo "  - content_writer: Content generation pipeline"
echo ""
echo "🔗 Server will be available at: http://127.0.0.1:8123"
echo "📈 LangSmith Project: agentic-ai-platform"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
uv run langgraph dev --port 8123 --no-browser

echo ""
echo "👋 Server stopped"
