from deepcontext.providers.config import ConfigProvider
ConfigProvider.load_config()
from deepcontext.providers.embedding_model import EmbeddingModelProvider
EmbeddingModelProvider.load_model()
from deepcontext.providers.nlp import NlpModelsProvider
NlpModelsProvider.load_models() 
from deepcontext.providers.llm import LLMProvider
LLMProvider.initialize_client()