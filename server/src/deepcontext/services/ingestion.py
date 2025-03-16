from deepcontext.utils.filesystem import FileUtils
from deepcontext.utils.chunk import ChunkUtils
from deepcontext.providers.vectordb import VectorDatabaseProvider
from deepcontext.providers.config import ConfigProvider
from flask import request, Response
class IngestionOrchestratorService:
    def start_ingestion():
        try:
            print("Starting new Ingestion process..")
            pdf_file_directory = ConfigProvider.get("PDF_FILE_DIRECTORY")
            VectorDatabaseProvider.delete_vectordb()
            FileUtils.format_directory(ConfigProvider.get("PDF_FILE_DIRECTORY"))
            print("Cleared PDF and DB folders")
            pdf_file_objects = [obj for obj in request.files.values()]
            FileUtils.persist_files_in_directory(pdf_file_objects, pdf_file_directory)
            print("Saved PDFs in folder")
            pdf_paths = [pdf_file_directory + file_object.filename for file_object in pdf_file_objects]
            chunks = ChunkUtils.create_chunks(pdf_paths)
            print("Generated Paragraph Chunks from PDFs")
            return Response(VectorDatabaseProvider.create_vectordb(chunks), mimetype="text/event-stream")
        except Exception as e:
            print("Error in IngestionOrchestratorService's start_ingestion", str(e))
            raise e