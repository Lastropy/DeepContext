from deepcontext.providers.config import ConfigProvider
from openai import OpenAI
from deepcontext.utils.chunk import ChunkUtils
from typing import List, Dict

class LLMProvider:
    """
    A provider class to initialize and interact with an LLM client.
    """
    
    llm_client = None  # Holds the initialized LLM client
    
    @staticmethod
    def initialize_client():
        """
        Initializes the LLM client using environment variables.
        """
        try:
            print("Initializing LLM Client...")
            LLMProvider.llm_client = OpenAI(
                base_url=ConfigProvider.get("LLM_URL"),  # Fetch LLM URL
                api_key=ConfigProvider.get("LLM_SECRET_KEY"),  # Fetch API key
            )
            print("LLM Client Generated")
        except Exception as e:
            raise e
    
    @staticmethod
    def call_llm(prompts: List[Dict]) -> str:
        """
        Calls the LLM with provided prompts.
        
        Args:
            prompts (list): A list of message dictionaries to send to the LLM.
        
        Returns:
            str: The LLM response text.
        
        Raises:
            Exception: If the LLM client is not initialized.
        """
        try:
            print("Calling LLM") 
            if LLMProvider.llm_client is None:
                raise Exception("LLM Client not initialized before use.")
            completion = LLMProvider.llm_client.chat.completions.create(
                model=ConfigProvider.get("LLM_NAME"),  # Fetch model name
                messages=prompts
            )
            return completion.choices[0].message.content  # Extract response content
        except Exception as e:
            raise e
    
    @staticmethod
    def rephrase_passage(text: str) -> str:
        """
        Rephrases a given passage while maintaining continuity.
        
        Args:
            text (str): The passage to rephrase.
        
        Returns:
            str: The rephrased passage.
        """
        try:
            print("Rephrasing passage")
            rephrase_prompt = """You will be given a part of a document along with a rephrased version of its previous part.
                                  Ensure that the new rephrased version maintains continuity with the previous part.
                                  
                                  Previous part: "{previous_rephrased}"
                                  Next part to rephrase: "{chunk}"
                                  
                                  Rephrased text should be easy to understand, unambiguous, have good grammar and simple wording.
                                  Provide a well-connected and natural-sounding rephrased version.
                                  Make sure to only provide the rephrased text as output.
                                  Keep the rephrased version of the text short.
                                  """
            rephrased_chunks = []
            previous_rephrased = ""
            chunks = ChunkUtils.break_paragraph_into_smaller_chunks(text)
            
            for chunk_no, chunk in enumerate(chunks, start=1):
                print(f"Rephrasing chunk {chunk_no}")
                prompts = [{
                    "role": "user",
                    "content": rephrase_prompt.format(previous_rephrased=previous_rephrased, chunk=chunk)
                }]
                rephrased_text = LLMProvider.call_llm(prompts)
                rephrased_chunks.append(rephrased_text)
                previous_rephrased = rephrased_text
            
            print("Rephrased Text")
            return " ".join(rephrased_chunks)
        except Exception as e:
            print("Error during rephrasing passage")
            raise e
    
    @staticmethod
    def summarize_passage(text: str, summary_length: str) -> str:
        """
        Summarizes a given passage while maintaining continuity.
        
        Args:
            text (str): The passage to summarize.
            summary_length (str): The desired summary length.
        
        Returns:
            str: The summarized passage.
        """
        try:
            print("Summarizing passage")
            summarize_prompt = """You will be given a part of a document along with a summarized version of its previous part.
                                  Ensure that the new summarized version maintains continuity with the previous part.
                                  
                                  Previous part: "{previous_summarized}"
                                  Next part to summarize: "{chunk}"
                                  
                                  Summarized text should be concise, well-structured, and retain key technical details.
                                  Provide a well-connected and natural-sounding {summary_length} summary.
                                  Make sure to only provide the summarized text as output.
                                  """
            summarized_chunks = []
            previous_summarized = ""
            chunks = ChunkUtils.break_paragraph_into_smaller_chunks(text)
            
            for chunk_no, chunk in enumerate(chunks, start=1):
                print(f"Summarizing chunk {chunk_no}")
                prompts = [{
                    "role": "user",
                    "content": summarize_prompt.format(previous_summarized=previous_summarized, chunk=chunk, summary_length=summary_length)
                }]
                summarized_text = LLMProvider.call_llm(prompts)
                summarized_chunks.append(summarized_text)
                previous_summarized = summarized_text
            
            print("Summarized Text")
            return " ".join(summarized_chunks)
        except Exception as e:
            print("Error during summarizing passage")
            raise e
