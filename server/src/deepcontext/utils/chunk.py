import pymupdf
import re
from langchain.docstore.document import Document
from nltk.tokenize import sent_tokenize
from deepcontext.constants.main import MAX_LLM_CHUNK_SIZE, OVERLAP_SENTENCES_WITHIN_CONSECUTIVE_CHUNKS
from typing import List

class ChunkUtils:
    """
    Utility class for handling document chunking operations.
    """

    @staticmethod
    def create_chunks(pdf_paths: List[str]) -> List[Document]:
        """
        Extracts text from PDF files and creates document chunks.

        Args:
            pdf_paths (List[str]): List of paths to PDF files.

        Returns:
            List[Document]: A list of Document objects containing chunked text.
        """
        chunks: List[Document] = []
        
        for pdf_path in pdf_paths:
            try:
                doc = pymupdf.open(pdf_path)
                document_name: str = pdf_path.split('/')[-1]  # Extract filename
                
                # Iterate over each page in the document
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text_blocks = page.get_text("blocks")  # Extract text blocks
                    
                    for block in text_blocks:
                        para_text: str = re.sub(r'\n+', '\n', block[4]).strip()
                        chunk = Document(
                            page_content=para_text,
                            metadata={
                                "source": document_name,
                                "page_number": page_num + 1
                            }
                        )
                        chunks.append(chunk)
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                raise e
        
        return chunks

    @staticmethod
    def break_paragraph_into_smaller_chunks(text: str) -> List[str]:
        """
        Breaks a paragraph into smaller chunks while maintaining readability.

        Args:
            text (str): The paragraph text to be chunked.

        Returns:
            List[str]: A list of chunked text segments.
        """
        print(f"Breaking paragraph of length {len(text)} into smaller chunks")
        sentences: List[str] = sent_tokenize(text)
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length: int = 0

        for i, sentence in enumerate(sentences):
            sentence_length: int = len(sentence.split())

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