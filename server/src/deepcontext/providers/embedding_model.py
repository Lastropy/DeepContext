from langchain_huggingface import HuggingFaceEmbeddings
from deepcontext.providers.config import ConfigProvider
import json

class EmbeddingModelProvider:
    embedding_model = None
    
    def load_model():
        try: 
            print("Loading Embedding Model...")
            EmbeddingModelProvider.embedding_model = HuggingFaceEmbeddings(
                model_name=ConfigProvider.get("EMBEDDINGS_MODEL_NAME"),
                model_kwargs=json.loads(ConfigProvider.get("EMBEDDINGS_MODEL_KWARGS")),
                encode_kwargs=json.loads(ConfigProvider.get("EMBEDDINGS_MODEL_ENCODING_KWARGS"))
            )
            print("Embedding Model loaded")
        except Exception as e:
            raise e
