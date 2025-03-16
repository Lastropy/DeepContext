import spacy 
import language_tool_python
import nltk

class NlpModelsProvider:
    """
    A provider class to load and manage the NLP models.
    """
     
    nlp_model = None
    language_tool = None
    def load_models():
        """
        Loads the NLP models.
        """
        try:
            print("Loading NLP Models...")
            NlpModelsProvider.nlp_model = spacy.load("en_core_web_sm") # For Checking Semantic Structure of Text
            NlpModelsProvider.language_tool = language_tool_python.LanguageTool('en-US') # For Checking Grammer of Text
            nltk.download('punkt') # For Constructing Smaller chunks to be sent to LLM
            print("NLP Models Loaded")
        except Exception as e:
            raise e
