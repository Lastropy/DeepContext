from langchain_huggingface import HuggingFaceEmbeddings
from deepcontext.providers.config import ConfigProvider
import json

class EmbeddingModelProvider:
    """
    A provider class to load and manage the embedding model.
    """
    
    embedding_model = None  # Holds the loaded embedding model
    
    @staticmethod
    def load_model():
        """
        Loads the embedding model using parameters from environment variables.
        """
        try: 
            print("Loading Embedding Model...")
            EmbeddingModelProvider.embedding_model = HuggingFaceEmbeddings(
                model_name=ConfigProvider.get("EMBEDDINGS_MODEL_NAME"),  # Fetch model name
                model_kwargs=json.loads(ConfigProvider.get("EMBEDDINGS_MODEL_KWARGS")),  # Fetch model kwargs
                encode_kwargs=json.loads(ConfigProvider.get("EMBEDDINGS_MODEL_ENCODING_KWARGS"))  # Fetch encoding kwargs
            )
            print("Embedding Model loaded")
        except Exception as e:
            raise e