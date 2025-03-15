from flask import jsonify
from deepcontext.services.ingestion import IngestionOrchestratorService

class IngestionController:
    def create_new_ingestion():
        try:
            return IngestionOrchestratorService.start_ingestion()
        except Exception as e: 
            return jsonify({"message": "Error during ingestion","error": str(e)}), 400