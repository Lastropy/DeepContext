from deepcontext.providers.config import ConfigProvider
from openai import OpenAI
from deepcontext.utils.chunk import ChunkUtils

class LLMProvider:
    llm_client = None
    
    def initialize_client():
      try:
        print("Initialising LLM Client...")
        LLMProvider.llm_client = OpenAI(
          base_url=ConfigProvider.get("LLM_URL"),
          api_key=ConfigProvider.get("LLM_SECRET_KEY"),
        )
        print("LLM Client Generated")
      except Exception as e:
        raise e

    def call_llm(prompts):
      try:
        print("Calling LLM") 
        if LLMProvider.llm_client is None:
          raise Exception("LLM Client not initialised before using.")
        completion = LLMProvider.llm_client.chat.completions.create(
          model=ConfigProvider.get("LLM_NAME"),
          messages=prompts
        )
        return completion.choices[0].message.content
      except Exception as e:
        raise e
      
    def rephrase_passage(text):
      try:
        print("Rephrasing passage")
        rephrase_prompt = """You will be given a part of a document along with a rephrased version of its previous part.
                              Ensure that the new rephrased version maintains continuity with the previous part.
                              
                              Previous part: "{previous_rephrased}"
                              Next part to rephrase: "{chunk}"
                              
                              Rephrased text should be easy to understand, unambiguous, have good grammar and simple wording.
                              Provide a well-connected and natural-sounding rephrased version.
                              Make sure to only provide the rephrased text as output.
                              Make sure to keep the rephrased version of the text short.
                              """
        rephrased_chunks = []
        previous_rephrased = ""
        chunks = ChunkUtils.break_paragraph_into_smaller_chunks(text)
        chunk_no = 1
        for chunk in chunks:
            print(f"Rephrasing chunk {chunk_no}")
            prompts = [{
              "role": "user",
              "content": rephrase_prompt.format(previous_rephrased=previous_rephrased, chunk=chunk)
            }]
            rephrased_text = LLMProvider.call_llm(prompts)
            rephrased_chunks.append(rephrased_text)
            previous_rephrased = rephrased_text
            chunk_no += 1
        print("Rephrased Text")
        return " ".join(rephrased_chunks)
        
      except Exception as e:
        print("Error during rephrasing passage")
        raise e
      
    def summarize_passage(text, summary_length):
      try:
        print("Summarizing passage")
        rephrase_prompt = """You will be given a part of a document along with a summarised version of its previous part.
                              Ensure that the new summarised version maintains continuity with the previous part.
                              
                              Previous part: "{previous_summarised}"
                              Next part to summarise: "{chunk}"
                              
                              Summarized text should be concise, well-structured and retaining key technical details.
                              Provide a well-connected and natural-sounding {summary_length} summary.
                              Make sure to only provide the summarised text as output.
                              """
        summarised_chunks = []
        previous_summarised = ""
        chunks = ChunkUtils.break_paragraph_into_smaller_chunks(text)
        chunk_no = 1
        for chunk in chunks:
            print(f"Summarising chunk {chunk_no}")
            prompts = [{
              "role": "user",
              "content": rephrase_prompt.format(previous_summarised=previous_summarised, chunk=chunk, summary_length=summary_length)
            }]
            summarised_text = LLMProvider.call_llm(prompts)
            summarised_chunks.append(summarised_text)
            previous_summarised = summarised_text
            chunk_no += 1
        print("Summarised Text")
        return " ".join(summarised_chunks)
        
      except Exception as e:
        print("Error during summarising passage")
        raise e
        

