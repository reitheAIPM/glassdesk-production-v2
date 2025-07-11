"""
Enhanced AI Interface for GlassDesk using LangChain
Provides RAG (Retrieval-Augmented Generation) capabilities for intelligent query processing
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import chromadb
from langchain_community.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
# NOTE: langchain_community.memory.ConversationBufferMemory does not exist as of 0.3.27; use langchain.memory instead.
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from .user_communication import user_comm
from .logging_config import log_api_error


class EnhancedAIInterface:
    """Enhanced AI interface using LangChain for RAG capabilities"""

    def __init__(self, data_processor):
        self.logger = logging.getLogger("glassdesk.enhanced_ai_interface")
        self.data_processor = data_processor
        self.user_comm = user_comm
        
        # Initialize LangChain components
        self.llm = ChatOpenAI(
            temperature=0.1,  # Lower temperature for more focused responses
            model_name="gpt-3.5-turbo",
            max_tokens=1000
        )
        
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize vector store
        self.vectorstore = None
        self.chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Conversation history
        self.conversation_history = []

    def initialize_vectorstore(self, documents: List[str] = None):
        """Initialize vector store with documents"""
        try:
            if not documents:
                # Create documents from processed data
                documents = self._create_documents_from_data()
            
            if not documents:
                self.logger.warning("No documents available for vector store initialization")
                return False
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Create vector store
            self.vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                collection_name="glassdesk_data"
            )
            
            # Create conversational chain
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}
                ),
                memory=self.memory,
                return_source_documents=True,
                verbose=False
            )
            
            self.logger.info(f"Vector store initialized with {len(texts)} text chunks")
            return True
            
        except Exception as e:
            log_api_error("initialize_vectorstore", e, {"document_count": len(documents) if documents else 0})
            self.user_comm.log_operation_error("initialize_vectorstore", e)
            return False

    def _create_documents_from_data(self) -> List[str]:
        """Create documents from processed data for vector store"""
        documents = []
        
        try:
            # Add email data
            gmail_data = self.data_processor.processed_data.get("gmail", {})
            if gmail_data:
                email_text = self._format_gmail_data(gmail_data)
                documents.append(f"Email Data:\n{email_text}")
            
            # Add meeting data
            zoom_data = self.data_processor.processed_data.get("zoom", {})
            if zoom_data:
                meeting_text = self._format_zoom_data(zoom_data)
                documents.append(f"Meeting Data:\n{meeting_text}")
            
            # Add task data
            asana_data = self.data_processor.processed_data.get("asana", {})
            if asana_data:
                task_text = self._format_asana_data(asana_data)
                documents.append(f"Task Data:\n{task_text}")
            
            # Add daily summary
            daily_summary = self.data_processor.create_daily_summary()
            if daily_summary:
                summary_text = self._format_daily_summary(daily_summary)
                documents.append(f"Daily Summary:\n{summary_text}")
            
            return documents
            
        except Exception as e:
            self.logger.error(f"Error creating documents from data: {e}")
            return []

    def _format_gmail_data(self, gmail_data: Dict) -> str:
        """Format Gmail data for document creation"""
        text = f"Total emails: {gmail_data.get('total_emails', 0)}\n"
        text += f"Important emails: {len(gmail_data.get('important_emails', []))}\n"
        text += f"Action items: {len(gmail_data.get('action_items', []))}\n"
        
        # Add important email details
        for email in gmail_data.get('important_emails', [])[:5]:  # Limit to 5
            text += f"- {email.get('subject', 'No subject')} from {email.get('sender', 'Unknown')}\n"
        
        return text

    def _format_zoom_data(self, zoom_data: Dict) -> str:
        """Format Zoom data for document creation"""
        text = f"Total meetings: {zoom_data.get('total_meetings', 0)}\n"
        text += f"Upcoming meetings: {len(zoom_data.get('upcoming_meetings', []))}\n"
        text += f"Past meetings: {len(zoom_data.get('past_meetings', []))}\n"
        text += f"Action items: {len(zoom_data.get('action_items', []))}\n"
        
        # Add meeting details
        for meeting in zoom_data.get('meeting_summaries', [])[:5]:  # Limit to 5
            text += f"- {meeting.get('title', 'No title')} on {meeting.get('date', 'Unknown date')}\n"
        
        return text

    def _format_asana_data(self, asana_data: Dict) -> str:
        """Format Asana data for document creation"""
        text = f"Total tasks: {asana_data.get('total_tasks', 0)}\n"
        text += f"Completed tasks: {len(asana_data.get('completed_tasks', []))}\n"
        text += f"Pending tasks: {len(asana_data.get('pending_tasks', []))}\n"
        text += f"Overdue tasks: {len(asana_data.get('overdue_tasks', []))}\n"
        text += f"High priority: {len(asana_data.get('high_priority', []))}\n"
        
        # Add task details
        for task in asana_data.get('high_priority', [])[:5]:  # Limit to 5
            text += f"- {task.get('name', 'No name')} (due: {task.get('due_date', 'No due date')})\n"
        
        return text

    def _format_daily_summary(self, summary: Dict) -> str:
        """Format daily summary for document creation"""
        text = f"Date: {summary.get('date', 'Unknown')}\n"
        text += f"Total action items: {len(summary.get('action_items', []))}\n"
        text += f"Priorities: {len(summary.get('priorities', []))}\n"
        text += f"Insights: {len(summary.get('insights', []))}\n"
        
        # Add insights
        for insight in summary.get('insights', [])[:3]:  # Limit to 3
            text += f"- {insight}\n"
        
        return text

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query using RAG capabilities"""
        try:
            self.logger.info(f"Processing enhanced query: {user_query}")

            # Add to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user_query": user_query,
                "type": "user"
            })

            # Initialize vector store if not already done
            if not self.vectorstore:
                success = self.initialize_vectorstore()
                if not success:
                    return self._fallback_response(user_query)

            # Process query with LangChain
            if self.chain:
                response = self.chain({"question": user_query})
                
                # Extract response and sources
                answer = response.get("answer", "I couldn't find a specific answer to your question.")
                source_documents = response.get("source_documents", [])
                
                # Format sources
                sources = []
                for doc in source_documents:
                    sources.append({
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "metadata": doc.metadata
                    })
                
                # Add response to conversation history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "response": answer,
                    "sources": sources,
                    "type": "assistant"
                })
                
                self.user_comm.notify_user("Query processed successfully with enhanced AI", level="info")
                
                return {
                    "response": answer,
                    "type": "enhanced_ai",
                    "sources": sources,
                    "confidence": "high" if sources else "medium"
                }
            else:
                return self._fallback_response(user_query)

        except Exception as e:
            log_api_error("enhanced_process_query", e, {"query": user_query})
            self.user_comm.log_operation_error("enhanced_process_query", e)
            return self._fallback_response(user_query)

    def _fallback_response(self, query: str) -> Dict[str, Any]:
        """Fallback response when RAG is not available"""
        return {
            "response": "I'm having trouble accessing my enhanced capabilities right now. Let me try a simpler approach.",
            "type": "fallback",
            "suggestion": "Try asking about your emails, meetings, or tasks specifically."
        }

    def add_document(self, content: str, metadata: Dict = None):
        """Add a new document to the vector store"""
        try:
            if not self.vectorstore:
                self.initialize_vectorstore()
            
            if self.vectorstore:
                # Split the content
                texts = self.text_splitter.split_text(content)
                
                # Add to vector store
                self.vectorstore.add_texts(
                    texts=texts,
                    metadatas=[metadata or {}] * len(texts)
                )
                
                self.logger.info(f"Added {len(texts)} text chunks to vector store")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error adding document to vector store: {e}")
            return False

    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar content in the vector store"""
        try:
            if not self.vectorstore:
                return []
            
            results = self.vectorstore.similarity_search(query, k=k)
            
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": 0.8  # Placeholder - Chroma doesn't return scores by default
                })
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error searching vector store: {e}")
            return []

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history

    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.memory:
            self.memory.clear()

    def get_vector_store_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if not self.vectorstore:
                return {"status": "not_initialized"}
            
            # Get collection info
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "status": "initialized",
                "document_count": count,
                "embedding_model": "text-embedding-ada-002",
                "chunk_size": 1000,
                "chunk_overlap": 200
            }
            
        except Exception as e:
            self.logger.error(f"Error getting vector store stats: {e}")
            return {"status": "error", "error": str(e)}


# Global enhanced AI interface instance
enhanced_ai_interface = None  # Will be initialized when needed 