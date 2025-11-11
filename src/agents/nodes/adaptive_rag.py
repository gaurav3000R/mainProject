"""Adaptive RAG implementation for Redmine chatbot.

Adaptive RAG intelligently decides whether to:
1. Use direct retrieval (call tools immediately)
2. Use web search for general questions
3. Answer directly without tools

This improves efficiency and response quality.
"""

from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.llms.base import BaseLLM
from src.utils.logger import app_logger


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    
    datasource: Literal["redmine_tools", "web_search", "direct_answer"] = Field(
        ...,
        description="Given a user question, choose to route it to redmine_tools, web_search, or answer directly.",
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of why this datasource was chosen"
    )


class AdaptiveRAGRouter:
    """
    Adaptive RAG router that intelligently decides the best way to answer queries.
    
    Routes:
    - redmine_tools: Questions about projects, issues, time entries (needs real-time data)
    - web_search: General questions not in Redmine (definitions, how-tos, external info)
    - direct_answer: Simple questions, greetings, or when LLM has sufficient knowledge
    """
    
    def __init__(self, llm: BaseLLM):
        """
        Initialize Adaptive RAG router.
        
        Args:
            llm: Language model for routing decisions
        """
        self.llm = llm
        self.structured_llm = llm.get_client().with_structured_output(RouteQuery)
        app_logger.info("Initialized AdaptiveRAGRouter")
    
    async def route(self, query: str) -> RouteQuery:
        """
        Route a query to the appropriate datasource.
        
        Args:
            query: User query
            
        Returns:
            RouteQuery with datasource and reasoning
        """
        system_prompt = """You are an expert at routing user questions to the appropriate datasource.

You have access to three datasources:

1. **redmine_tools**: Use this for questions about:
   - Projects in Redmine (list projects, project details)
   - Issues (view, create, update, search issues)
   - Time entries (view time logs)
   - Metadata (statuses, priorities, trackers)
   - Any real-time Redmine data

2. **web_search**: Use this for:
   - General information not in Redmine
   - How-to guides or tutorials
   - Definitions or explanations
   - External information
   - Current events or news

3. **direct_answer**: Use this for:
   - Simple greetings or pleasantries
   - Questions about capabilities
   - Questions you can answer with general knowledge
   - Clarification questions
   - Simple conversational responses

Examples:
- "Show me all projects" → redmine_tools (needs real Redmine data)
- "What is Redmine?" → direct_answer (general knowledge)
- "How to set up CI/CD?" → web_search (external information)
- "Hello" → direct_answer (greeting)
- "What can you do?" → direct_answer (about capabilities)
- "Find issues about login" → redmine_tools (Redmine query)

Choose the most efficient datasource that will give the best answer."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}")
        ])
        
        chain = prompt | self.structured_llm
        result = await chain.ainvoke({"query": query})
        
        app_logger.info(f"Routed query to: {result.datasource} - {result.reasoning}")
        return result


class GradeDocuments(BaseModel):
    """Binary score for document relevance check."""
    
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )
    reasoning: str = Field(
        description="Brief explanation of the relevance decision"
    )


class HallucinationGrader(BaseModel):
    """Binary score for hallucination check."""
    
    binary_score: str = Field(
        description="Answer is grounded in facts, 'yes' or 'no'"
    )
    reasoning: str = Field(
        description="Brief explanation of the grading"
    )


class AnswerGrader(BaseModel):
    """Binary score for answer usefulness."""
    
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )
    reasoning: str = Field(
        description="Brief explanation of usefulness"
    )


class AdaptiveRAGGrader:
    """
    Grade documents, check hallucinations, and evaluate answer quality.
    Part of the Adaptive RAG system for self-correction.
    """
    
    def __init__(self, llm: BaseLLM):
        """Initialize graders."""
        self.llm = llm
        self.doc_grader = llm.get_client().with_structured_output(GradeDocuments)
        self.hallucination_grader = llm.get_client().with_structured_output(HallucinationGrader)
        self.answer_grader = llm.get_client().with_structured_output(AnswerGrader)
        app_logger.info("Initialized AdaptiveRAGGrader")
    
    async def grade_documents(self, question: str, documents: str) -> GradeDocuments:
        """
        Check if retrieved documents are relevant to the question.
        
        Args:
            question: User question
            documents: Retrieved documents/tool results
            
        Returns:
            GradeDocuments with relevance score
        """
        system_prompt = """You are a grader assessing relevance of retrieved documents to a user question.
        
If the documents contain information related to the user question, grade it as relevant.
Give a binary score 'yes' or 'no' to indicate whether the documents are relevant."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Question: {question}\n\nDocuments: {documents}\n\nAre these documents relevant?")
        ])
        
        chain = prompt | self.doc_grader
        result = await chain.ainvoke({"question": question, "documents": documents})
        
        app_logger.info(f"Document relevance: {result.binary_score} - {result.reasoning}")
        return result
    
    async def check_hallucination(self, documents: str, answer: str) -> HallucinationGrader:
        """
        Check if the answer is grounded in the documents.
        
        Args:
            documents: Source documents
            answer: Generated answer
            
        Returns:
            HallucinationGrader with grounding score
        """
        system_prompt = """You are a grader assessing whether an answer is grounded in facts from documents.
        
Give a binary score 'yes' or 'no'. 'yes' means the answer is grounded in the documents."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Documents: {documents}\n\nAnswer: {answer}\n\nIs the answer grounded in the documents?")
        ])
        
        chain = prompt | self.hallucination_grader
        result = await chain.ainvoke({"documents": documents, "answer": answer})
        
        app_logger.info(f"Hallucination check: {result.binary_score} - {result.reasoning}")
        return result
    
    async def grade_answer(self, question: str, answer: str) -> AnswerGrader:
        """
        Check if the answer addresses the question.
        
        Args:
            question: User question
            answer: Generated answer
            
        Returns:
            AnswerGrader with usefulness score
        """
        system_prompt = """You are a grader assessing whether an answer is useful to resolve a question.
        
Give a binary score 'yes' or 'no'. 'yes' means the answer addresses the question."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Question: {question}\n\nAnswer: {answer}\n\nDoes the answer address the question?")
        ])
        
        chain = prompt | self.answer_grader
        result = await chain.ainvoke({"question": question, "answer": answer})
        
        app_logger.info(f"Answer usefulness: {result.binary_score} - {result.reasoning}")
        return result
