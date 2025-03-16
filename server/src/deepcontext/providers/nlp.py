import spacy 
import language_tool_python
import nltk

class NlpModelsProvider:
    nlp_model = None
    language_tool = None
    def load_models():
        try:
            print("Loading NLP Models...")
            NlpModelsProvider.nlp_model = spacy.load("en_core_web_sm")
            NlpModelsProvider.language_tool = language_tool_python.LanguageTool('en-US')
            nltk.download('punkt')
            print("NLP Models Loaded")
        except Exception as e:
            raise e
