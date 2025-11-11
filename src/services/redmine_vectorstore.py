"""
Vector Store Service for Redmine Issue Descriptions.

Implements semantic search over issue content using ChromaDB.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from langchain_chroma import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

from src.utils.logger import app_logger


class RedmineVectorStore:
    """Vector store for semantic search over Redmine issues."""
    
    def __init__(
        self,
        persist_directory: str = "data/vectorstore/redmine",
        collection_name: str = "redmine_issues"
    ):
        """
        Initialize vector store.
        
        Args:
            persist_directory: Directory to persist vector database
            collection_name: Name of the collection
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.vectorstore: Optional[Chroma] = None
        self.embeddings = None
        
        if not CHROMA_AVAILABLE:
            app_logger.warning("ChromaDB not available. Vector search disabled.")
            return
        
        # Create directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings (using free local model)
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            app_logger.info("Initialized HuggingFace embeddings")
        except Exception as e:
            app_logger.error(f"Failed to initialize embeddings: {e}")
            return
        
        # Initialize vector store
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            app_logger.info(f"Initialized Chroma vectorstore at {self.persist_directory}")
        except Exception as e:
            app_logger.error(f"Failed to initialize vectorstore: {e}")
    
    def is_available(self) -> bool:
        """Check if vector store is available."""
        return self.vectorstore is not None
    
    def load_from_metadata(self, metadata_file: str = "redminDocs/redmine_metadata.json"):
        """
        Load and index issues from metadata JSON.
        
        Args:
            metadata_file: Path to metadata JSON file
        """
        if not self.is_available():
            app_logger.warning("Vector store not available")
            return
        
        try:
            # Load metadata
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            issues = metadata.get('endpoints', {}).get('getIssues', {}).get('data', [])
            
            if not issues:
                app_logger.warning("No issues found in metadata")
                return
            
            app_logger.info(f"Loading {len(issues)} issues into vector store...")
            
            # Create documents from issues
            documents = []
            for issue in issues:
                # Create content with all relevant information
                content_parts = [
                    f"Issue #{issue['id']}: {issue.get('subject', '')}",
                    f"Project: {issue.get('project', {}).get('name', '')}",
                    f"Tracker: {issue.get('tracker', {}).get('name', '')}",
                    f"Status: {issue.get('status', {}).get('name', '')}",
                    f"Priority: {issue.get('priority', {}).get('name', '')}",
                ]
                
                # Add description if available
                description = issue.get('description', '')
                if description:
                    content_parts.append(f"Description: {description}")
                
                content = "\n".join(content_parts)
                
                # Create document with metadata
                doc = Document(
                    page_content=content,
                    metadata={
                        "issue_id": issue['id'],
                        "subject": issue.get('subject', ''),
                        "project_id": issue.get('project', {}).get('id'),
                        "project_name": issue.get('project', {}).get('name', ''),
                        "tracker": issue.get('tracker', {}).get('name', ''),
                        "status": issue.get('status', {}).get('name', ''),
                        "priority": issue.get('priority', {}).get('name', ''),
                        "created_on": issue.get('created_on', ''),
                        "updated_on": issue.get('updated_on', ''),
                        "type": "issue"
                    }
                )
                documents.append(doc)
            
            # Split documents if too large
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            split_docs = text_splitter.split_documents(documents)
            
            # Add to vector store
            self.vectorstore.add_documents(split_docs)
            
            app_logger.info(f"✅ Loaded {len(issues)} issues ({len(split_docs)} chunks) into vector store")
            
        except Exception as e:
            app_logger.error(f"Failed to load issues into vector store: {e}")
    
    def load_projects_from_metadata(self, metadata_file: str = "redminDocs/redmine_metadata.json"):
        """
        Load project descriptions into vector store (for long descriptions).
        
        Args:
            metadata_file: Path to metadata JSON file
        """
        if not self.is_available():
            return
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            projects = metadata.get('endpoints', {}).get('getProjects', {}).get('data', [])
            
            if not projects:
                return
            
            documents = []
            for project in projects:
                description = project.get('description', '')
                
                # Only add if description is substantial
                if len(description) > 100:
                    content = f"Project: {project['name']}\nDescription: {description}"
                    
                    doc = Document(
                        page_content=content,
                        metadata={
                            "project_id": project['id'],
                            "project_name": project['name'],
                            "identifier": project.get('identifier', ''),
                            "type": "project"
                        }
                    )
                    documents.append(doc)
            
            if documents:
                self.vectorstore.add_documents(documents)
                app_logger.info(f"✅ Loaded {len(documents)} project descriptions into vector store")
                
        except Exception as e:
            app_logger.error(f"Failed to load projects: {e}")
    
    def semantic_search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search over issues.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of search results with metadata
        """
        if not self.is_available():
            return []
        
        try:
            # Perform similarity search
            results = self.vectorstore.similarity_search_with_score(
                query,
                k=k,
                filter=filter_dict
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                result = {
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata
                }
                formatted_results.append(result)
            
            app_logger.info(f"Semantic search for '{query}': {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            app_logger.error(f"Semantic search failed: {e}")
            return []
    
    def search_similar_issues(
        self,
        issue_id: int,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find issues similar to a given issue.
        
        Args:
            issue_id: Issue ID to find similar issues for
            k: Number of results
            
        Returns:
            List of similar issues
        """
        if not self.is_available():
            return []
        
        try:
            # Get the issue content first
            results = self.vectorstore.get(
                where={"issue_id": issue_id}
            )
            
            if not results or not results['documents']:
                return []
            
            # Use the issue content as query
            query_content = results['documents'][0]
            
            # Find similar
            similar = self.semantic_search(
                query_content,
                k=k+1  # +1 to exclude self
            )
            
            # Filter out the original issue
            similar = [s for s in similar if s['metadata'].get('issue_id') != issue_id][:k]
            
            return similar
            
        except Exception as e:
            app_logger.error(f"Failed to find similar issues: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        if not self.is_available():
            return {"available": False}
        
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "available": True,
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": str(self.persist_directory)
            }
        except Exception as e:
            app_logger.error(f"Failed to get stats: {e}")
            return {"available": True, "error": str(e)}
    
    def refresh(self):
        """Refresh vector store from latest metadata."""
        if not self.is_available():
            return
        
        try:
            # Clear existing data
            self.vectorstore.delete_collection()
            
            # Reinitialize
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            
            # Reload data
            self.load_from_metadata()
            self.load_projects_from_metadata()
            
            app_logger.info("✅ Vector store refreshed")
            
        except Exception as e:
            app_logger.error(f"Failed to refresh vector store: {e}")


# Global vector store instance
redmine_vectorstore = RedmineVectorStore()
