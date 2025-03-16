from deepcontext.providers.vectordb import VectorDatabaseProvider
from deepcontext.providers.llm import LLMProvider
from deepcontext.constants.main import GENERIC_MESSAGE_FOR_NO_CHUNK_CASE, PASSAGE_CONFIDENCE_SCORE
from deepcontext.utils.readability_metrics import ReadabilityUtils
from flask import request, jsonify, Response
from typing import Dict, Any

class ContextualSearchOrchestratorService:
    """
    Service to orchestrate contextual search operations.
    It retrieves relevant passages from a vector database,
    checks readability, and applies rephrasing or summarization if needed.
    """
    
    @staticmethod
    def start_searching() -> Response:
        """
        Handles the contextual search process by querying the vector database,
        evaluating passage readability, and summarizing if necessary.
        Returns a JSON response with the retrieved passage and metadata.
        """
        try:
            # Load the vector database provider
            VectorDatabaseProvider.load_vectordb()
            request_body = request.get_json()
            # Validate request payload
            if "query" not in request_body or "summary_length" not in request_body:
                raise ValueError("The query or summary length is missing from the request body.")
            
            query: str = request_body["query"]
            summary_length: int = request_body["summary_length"]
            
            print("Querying vector database...")
            search_results = VectorDatabaseProvider.search_vectordb(query)
            
            if not search_results:
                return jsonify({"message": "No passages found", "data": {}})
            
            retrieved_passage, confidence_score = search_results[0]
            
            # Handle cases where the retrieved passage has low confidence
            if confidence_score < PASSAGE_CONFIDENCE_SCORE:
                return jsonify({"message": "Low confidence in retrieved passage", "data": {"passage_content": GENERIC_MESSAGE_FOR_NO_CHUNK_CASE}})
            
            passage_content: str = retrieved_passage.page_content
            metadata: Dict[str, Any] = {
                "document_name": retrieved_passage.metadata.get("source", "Unknown"),
                "page_number": retrieved_passage.metadata.get("page_number", "N/A")
            }
            
            # Check if the passage is unclear and rephrase if necessary
            if ReadabilityUtils.check_unclear_text(passage_content):
                passage_content = LLMProvider.rephrase_passage(passage_content)
            
            # Check if the passage is too long and summarize if needed
            if ReadabilityUtils.check_if_too_long(passage_content):
                passage_content = LLMProvider.summarize_passage(passage_content, summary_length)
            
            return jsonify({
                "message": "Successfully retrieved passage",
                "data": {
                    "passage_content": passage_content,
                    "metadata": metadata
                }
            })
        
        except Exception as error:
            print(f"Error in ContextualSearchOrchestratorService's start_searching: {error}")
            raise error
