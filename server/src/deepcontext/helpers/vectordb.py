from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from deepcontext import embedding_model

def create_vectordb(chunks, vector_database_directory):
    vectordb = None
    last_sent_progress = -1
    update_threshold = 1
    with tqdm(total=len(chunks), desc="Progress", unit=" chunks") as pbar:
        for i, chunk in enumerate(chunks):
            if vectordb is not None: vectordb.add_documents(documents=[chunk])
            else: vectordb = FAISS.from_documents(documents=[chunk], embedding=embedding_model)
            pbar.update(1) 
            progress = int((i + 1) / len(chunks) * 100)
            if progress >= last_sent_progress + update_threshold:
                yield f"data: {progress}% chunks indexed\n\n"
                last_sent_progress = progress                
    vectordb.save_local(vector_database_directory)
    yield "data: 100% chunks indexed\n\n"
    