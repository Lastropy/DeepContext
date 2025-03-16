from deepcontext.utils.filesystem import FileUtils
from deepcontext.utils.chunk import ChunkUtils
from deepcontext.providers.vectordb import VectorDatabaseProvider
from deepcontext.providers.config import ConfigProvider
from flask import request, Response

class IngestionOrchestratorService:
    """
    Service class for orchestrating the ingestion process of PDF documents into the vector database.
    """
    
    @staticmethod
    def start_ingestion() -> Response:
        """
        Initiates the ingestion process by clearing the existing database, processing uploaded PDF files,
        generating text chunks, and indexing them in the vector database.
        
        Returns:
            Response: A streaming response indicating the progress of indexing.
        
        Raises:
            Exception: If any step in the ingestion process fails.
        """
        try:
            print("Starting new Ingestion process...")
            if len(request.files) == 0:
                raise Exception("Files not provided for ingestion")
        
            pdf_file_directory = ConfigProvider.get("PDF_FILE_DIRECTORY")
            
            # Clear existing vector database and PDF storage
            VectorDatabaseProvider.delete_vectordb()
            FileUtils.format_directory(pdf_file_directory)
            print("Cleared PDF and DB folders")
            
            # Retrieve uploaded PDF files from request
            pdf_file_objects = [obj for obj in request.files.values()]
            
            # Persist uploaded PDFs in the designated directory
            FileUtils.persist_files_in_directory(pdf_file_objects, pdf_file_directory)
            print("Saved PDFs in folder")
            
            # Generate file paths for the saved PDFs
            pdf_paths = [pdf_file_directory + file_object.filename for file_object in pdf_file_objects]
            
            # Convert PDFs into text chunks
            chunks = ChunkUtils.create_chunks(pdf_paths)
            print("Generated Paragraph Chunks from PDFs")
            
            # Start indexing the chunks into the vector database and return progress as a stream
            return Response(VectorDatabaseProvider.create_vectordb(chunks), mimetype="text/event-stream")
        
        except Exception as e:
            print("Error in IngestionOrchestratorService's start_ingestion", str(e))
            raise e