import os
from deepcontext.common.llm import llm_client

def call_llm(prompts):
#     prompts = [
#     {
#         "role": "user",
#         "content": '''Write a poem for my casual girlfriend'''
#     }
# ]
    completion = llm_client.chat.completions.create(
        model=os.environ["LLM_NAME"],
        messages=prompts
    )
    return completion.choices[0].message.content