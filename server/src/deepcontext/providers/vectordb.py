from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from deepcontext.providers.config import ConfigProvider
from deepcontext.providers.embedding_model import EmbeddingModelProvider
from deepcontext.utils.filesystem import FileUtils

class VectorDatabaseProvider:
    vectordb = None
    def create_vectordb(chunks):
        try:
            print("Creating new VectorDB...")
            vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
            last_sent_progress = -1
            update_threshold = 1
            with tqdm(total=len(chunks), desc="Progress", unit=" chunks") as progress_bar:
                for i, chunk in enumerate(chunks):
                    if VectorDatabaseProvider.vectordb is not None: 
                        VectorDatabaseProvider.vectordb.add_documents(documents=[chunk])
                    else: 
                        VectorDatabaseProvider.vectordb = FAISS.from_documents(documents=[chunk], embedding=EmbeddingModelProvider.embedding_model)
                    progress_bar.update(1) 
                    progress = int((i + 1) / len(chunks) * 100)
                    if progress >= last_sent_progress + update_threshold:
                        yield f"data: {progress}% chunks indexed\n\n"
                        last_sent_progress = progress                
            VectorDatabaseProvider.vectordb.save_local(vector_database_directory)
            print("New VectorDB Created")
            yield "data: 100% chunks indexed\n\n"
        except Exception as e:
            raise e
    
    def load_vectordb():
        try:
            if VectorDatabaseProvider.vectordb is None:
                vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
                VectorDatabaseProvider.vectordb = FAISS.load_local(vector_database_directory, embeddings=EmbeddingModelProvider.embedding_model, allow_dangerous_deserialization=True)
        except Exception as e:
            raise e

    def search_vectordb(text):
        try:
            if VectorDatabaseProvider.vectordb is None:
                raise Exception("Vector DB not initialised before searching")
            passage_retrieved = VectorDatabaseProvider.vectordb.similarity_search_with_relevance_scores(query = text, k = 1)
            return passage_retrieved
        except Exception as e:
            raise e
        
    def delete_vectordb():
        try:
            VectorDatabaseProvider.vectordb = None
            vector_database_directory = ConfigProvider.get("FAISS_DATABASE_DIRECTORY")
            FileUtils.format_directory(vector_database_directory)
        except Exception as e:
            raise e