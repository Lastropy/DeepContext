from deepcontext.helpers.filesystem import update_directory, persist_files_in_directory
from deepcontext.helpers.chunk import create_chunks
from deepcontext.helpers.vectordb import create_vectordb
import os
from flask import request, Response

class IngestionOrchestratorService:
    def start_ingestion():
        try:
            save_documents_directory,databases_directory, vector_database_directory = os.environ["PDF_FILE_DIRECTORY"], os.environ["DATABASES_DIRECTORY"], os.environ["FAISS_DATABASE_DIRECTORY"]
            update_directory(save_documents_directory)
            update_directory(databases_directory)
            update_directory(vector_database_directory)
            pdf_file_objects = [obj for obj in request.files.values()]
            persist_files_in_directory(pdf_file_objects, save_documents_directory)
            pdf_paths = [save_documents_directory + file_object.filename for file_object in pdf_file_objects]
            chunks = create_chunks(pdf_paths)
            return Response(create_vectordb(chunks, vector_database_directory), mimetype="text/event-stream")
        except Exception as e:
            print("Error in IngestionOrchestratorService's start_ingestion", str(e))
            raise e