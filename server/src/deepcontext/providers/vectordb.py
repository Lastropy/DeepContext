from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from deepcontext.providers.config import ConfigProvider
from deepcontext.providers.embedding_model import EmbeddingModelProvider
from deepcontext.utils.filesystem import FileUtils
from typing import List

class VectorDatabaseProvider:
    """
    A provider class for managing a FAISS-based vector database.
    """
    
    vectordb = None  # Holds the initialized vector database
    
    @staticmethod
    def create_vectordb(chunks: List[Document]):
        """
        Creates a new FAISS vector database and indexes the provided document chunks.
        
        Args:
            chunks (list): A list of Document objects to index.
        
        Yields:
            str: Progress updates on indexing.
        """
        try:
            print("Creating new VectorDB...")
            vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
            last_sent_progress = -1
            update_threshold = 1
            
            with tqdm(total=len(chunks), desc="Progress", unit=" chunks") as progress_bar:
                for i, chunk in enumerate(chunks):
                    if VectorDatabaseProvider.vectordb is not None: 
                        VectorDatabaseProvider.vectordb.add_documents(documents=[chunk])  # Add document to existing DB
                    else: 
                        VectorDatabaseProvider.vectordb = FAISS.from_documents(documents=[chunk], embedding=EmbeddingModelProvider.embedding_model)  # Create new DB
                    
                    progress_bar.update(1)
                    progress = int((i + 1) / len(chunks) * 100) # Chunk ingestion progress calculated as percentage
                    
                    # Update Client on each 1% increase in Chunk ingestion Percentage
                    if progress >= last_sent_progress + update_threshold:
                        yield f"data: {progress}% chunks indexed\n\n"
                        last_sent_progress = progress                
            
            VectorDatabaseProvider.vectordb.save_local(vector_database_directory)  # Save DB locally
            print("New VectorDB Created")
            yield "data: 100% chunks indexed\n\n"
        except Exception as e:
            raise e
    
    @staticmethod
    def load_vectordb():
        """
        Loads the FAISS vector database from local storage.
        """
        try:
            if VectorDatabaseProvider.vectordb is None:
                vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
                VectorDatabaseProvider.vectordb = FAISS.load_local(vector_database_directory, embeddings=EmbeddingModelProvider.embedding_model, allow_dangerous_deserialization=True)
        except Exception as e:
            raise e

    @staticmethod
    def search_vectordb(text: str) -> List[Document]:
        """
        Searches the vector database for the most relevant document based on similarity.
        
        Args:
            text (str): The query text to search for.
        
        Returns:
            list: A list of retrieved Document objects with relevance scores.
        
        Raises:
            Exception: If the vector database is not initialized.
        """
        try:
            if VectorDatabaseProvider.vectordb is None:
                raise Exception("Vector DB not initialized before searching")
            
            passage_retrieved = VectorDatabaseProvider.vectordb.similarity_search_with_relevance_scores(query=text, k=1)  # Search DB
            return passage_retrieved
        except Exception as e:
            raise e
        
    @staticmethod
    def delete_vectordb():
        """
        Deletes the vector database by resetting the instance and clearing stored files.
        """
        try:
            VectorDatabaseProvider.vectordb = None  # Reset the database
            vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
            FileUtils.format_directory(vector_database_directory)  # Clear stored files
        except Exception as e:
            raise e
