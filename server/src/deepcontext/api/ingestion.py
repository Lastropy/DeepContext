from deepcontext import app
from deepcontext.controller.ingestion import IngestionController

@app.route("/ingestion", methods=["POST"])
def ingestion_endpoint():
    return IngestionController.create_new_ingestion()
