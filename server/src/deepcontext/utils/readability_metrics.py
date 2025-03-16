from deepcontext.providers.nlp import NlpModelsProvider
from deepcontext.constants.main import REPHRASE_PASSAGE_THRESHOLD
import textstat
from typing import Any

class ReadabilityUtils:
    """
    Utility class for analyzing text readability, grammar, and ambiguity.
    """

    @staticmethod
    def check_unclear_text(text: str) -> bool:
        """
        Determines if the text is unclear based on readability scores, grammar issues,
        sentence length, and passive voice usage.

        Args:
            text (str): The text to analyze.

        Returns:
            bool: True if the text is considered unclear, False otherwise.
        """
        try:
            # Readability scores
            flesch_score: float = textstat.flesch_reading_ease(text)
            fog_index: float = textstat.gunning_fog(text)

            # Grammar mistakes
            grammar_errors: Any = NlpModelsProvider.language_tool.check(text)
            num_grammar_errors: int = len(grammar_errors)

            # Check for ambiguity (long sentences, passive voice, unclear references)
            doc = NlpModelsProvider.nlp_model(text)
            num_long_sentences: int = sum(1 for sent in doc.sents if len(sent) > 20)
            num_passive_voice: int = sum(1 for token in doc if token.dep_ == "auxpass")
            
            # Decision criteria for unclear text
            unclear: bool = (
                (flesch_score < 50 and fog_index > 15) or  # Hard to read, high complexity
                (num_grammar_errors > 2) or  # Poor grammar
                (num_long_sentences > 2 and num_passive_voice > 2)  # Lengthy sentences & passive voice
            )
            
            return unclear
        except Exception as e:
            raise Exception(f"Error analyzing text readability: {e}")

    @staticmethod
    def check_if_too_long(text: str) -> bool:
        """
        Checks if the text exceeds the defined length constraint for readability.

        Args:
            text (str): The text to evaluate.

        Returns:
            bool: True if the text is too long, False otherwise.
        """
        try:
            return len(text) > REPHRASE_PASSAGE_THRESHOLD
        except Exception as e:
            raise Exception(f"Error checking text length: {e}")
