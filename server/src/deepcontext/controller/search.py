from flask import jsonify
from deepcontext.services.search import ContextualSearchOrchestratorService

class ContextualSearchController:
    def start_new_search():
        try:
            return ContextualSearchOrchestratorService.start_searching()
        except Exception as e: 
            return jsonify({"message": "Error during search","error": str(e)}), 400