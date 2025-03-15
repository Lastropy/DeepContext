import os
from openai import OpenAI

llm_client = OpenAI(
  base_url=os.environ["LLM_URL"],
  api_key=os.environ["LLM_SECRET_KEY"],
)