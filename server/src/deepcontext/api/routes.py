from deepcontext import app
from deepcontext.controller.ingestion import IngestionController
from deepcontext.controller.search import ContextualSearchController

@app.route("/search", methods=["GET"])
def search_endpoint():
    return ContextualSearchController.start_new_search()

@app.route("/ingestion", methods=["POST"])
def ingestion_endpoint():
    return IngestionController.create_new_ingestion()
