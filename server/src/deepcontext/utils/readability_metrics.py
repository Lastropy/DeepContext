from deepcontext.providers.nlp import NlpModelsProvider
from deepcontext.constants.main import REPHRASE_PASSAGE_THRESHOLD
import textstat

class ReadabilityUtils:
    def check_unclear_text(text):
        try:
            """Analyzes text clarity based on readability, grammar, and ambiguity."""
            # Readability scores
            flesch_score = textstat.flesch_reading_ease(text)
            fog_index = textstat.gunning_fog(text)

            # Grammar mistakes
            grammar_errors = NlpModelsProvider.language_tool.check(text)
            num_grammar_errors = len(grammar_errors)

            # Check for ambiguity (long sentences, passive voice, unclear references)
            doc = NlpModelsProvider.nlp_model(text)
            num_long_sentences = sum(1 for sent in doc.sents if len(sent) > 20)
            num_passive_voice = sum(1 for token in doc if token.dep_ == "auxpass")
            
            # Decision criteria
            unclear = (
                # Hard to read and High complexity
                (flesch_score < 50 and fog_index > 15) or
                # Poor grammar
                (num_grammar_errors > 2) or
                # Lengthy sentences and Excessive passive voice
                (num_long_sentences > 2 and num_passive_voice > 2)
            )

            return unclear
        except Exception as e:
            raise e

    def check_if_too_long(text):
        try:
            length_constraint = REPHRASE_PASSAGE_THRESHOLD
            return len(text) > length_constraint
        except Exception as e:
            raise e
