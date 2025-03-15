from langchain_huggingface import HuggingFaceEmbeddings
import os
import json

print("Loading embedding model....")
embedding_model = HuggingFaceEmbeddings(
    model_name=os.environ["EMBEDDINGS_MODEL_NAME"],
    model_kwargs=json.loads(os.environ["EMBEDDINGS_MODEL_KWARGS"]),
    encode_kwargs=json.loads(os.environ["EMBEDDINGS_MODEL_ENCODING_KWARGS"])
)
print("Embedding model loaded!")