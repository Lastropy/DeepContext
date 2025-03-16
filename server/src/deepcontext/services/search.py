from deepcontext.providers.vectordb import VectorDatabaseProvider
from deepcontext.providers.llm import LLMProvider
from deepcontext.constants.main import GENERIC_MESSAGE_FOR_NO_CHUNK_CASE, PASSAGE_CONFIDENCE_SCORE
from deepcontext.utils.readability_metrics import ReadabilityUtils
from flask import request, jsonify

class ContextualSearchOrchestratorService:
    def start_searching():
        try:
            VectorDatabaseProvider.load_vectordb()
            print("Checking for valid keys")
            request_body = request.get_json()
            if "query" not in request_body or "summary_length" not in request_body:
                raise Exception("The query or summary length is not provided in the request body")
            print("Getting valid keys")
            query, summary_length = request_body["query"], request_body["summary_length"]
            print("Searching vectordb")
            passage_retrieved = VectorDatabaseProvider.search_vectordb(query)[0]
            if(passage_retrieved[1] < PASSAGE_CONFIDENCE_SCORE):
                passage_content = GENERIC_MESSAGE_FOR_NO_CHUNK_CASE
            else:
                passage_content = passage_retrieved[0].page_content
                document_name, page_number = passage_retrieved[0].metadata["source"], passage_retrieved[0].metadata["page_number"]
                unclear_passage = ReadabilityUtils.check_unclear_text(passage_content)
                if(unclear_passage):
                    rephrased_passage = LLMProvider.rephrase_passage(passage_content)
                    passage_content = rephrased_passage
                too_long_passage = ReadabilityUtils.check_if_too_long(passage_content)
                if(too_long_passage):
                    summarized_passage = LLMProvider.summarize_passage(passage_content, summary_length)
                    passage_content = summarized_passage
            return jsonify({"message": "Successfully retrieved passage", "data": {"passage_content":passage_content, "metadata": {"document_name": document_name, "page_number": page_number} }})
        except Exception as e:
            print("Error in ContextualSearchOrchestratorService's start_searching", str(e))
            raise e