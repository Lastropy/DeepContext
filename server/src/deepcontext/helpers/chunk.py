import pymupdf
import re
from glob import glob
from langchain.docstore.document import Document

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
            print(e)