import pymupdf
import re
from langchain.docstore.document import Document
from nltk.tokenize import sent_tokenize
from deepcontext.constants.main import MAX_LLM_CHUNK_SIZE, OVERLAP_SENTENCES_WITHIN_CONSECUTIVE_CHUNKS
class ChunkUtils:
    def create_chunks(pdf_paths):
        for pdf_path in pdf_paths:
            try: 
                doc = pymupdf.open(pdf_path)
                document_name = pdf_path.split('/')[-1]  # Extract document name (filename)
                chunks = []

                # Iterate over each page in the document
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text("blocks")  # Extract text in plain format
                    for block in text:
                        para_text = re.sub(r'\n+', '\n', block[4]).strip()
                        chunk = Document(page_content=para_text, metadata={ "source": document_name,"page_number": page_num + 1})
                        chunks.append(chunk)
                return chunks
            except Exception as e:
                raise e
            
    def break_paragraph_into_smaller_chunks(text):
        print("Breaking para of length", len(text), "into smaller chunks")
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        for i, sentence in enumerate(sentences):
            sentence_length = len(sentence.split())

            # If adding this sentence exceeds chunk size, finalize current chunk
            if current_length + sentence_length > MAX_LLM_CHUNK_SIZE:
                chunks.append(" ".join(current_chunk))

                # Start a new chunk with overlap
                current_chunk = sentences[max(0, i - OVERLAP_SENTENCES_WITHIN_CONSECUTIVE_CHUNKS):i]
                current_length = sum(len(s.split()) for s in current_chunk)
            
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        print(f"Divided text into {len(chunks)} chunks")
        return chunks
