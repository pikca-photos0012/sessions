import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
 
from PyPDF2 import PdfReader
data=r"C:\Users\labuser\Downloads\sessions\Policy-Wording-Acko-Retail-Health-Policy.pdf"
 
reader=PdfReader(data)
raw_text="\n".join([ page.extract_text() for page in reader.pages if page.extract_text()])
print(raw_text)
 
embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
 
 
def create_chunk(text,chunk_size=1000,overlap=200):
    chunk=[]
    start=0
    while start<len(text):
        end=start +chunk_size
        chunk.append(text[start:end])
        start+=chunk_size-overlap
    return chunk
 
chunk=create_chunk(raw_text)
 
 
doc_model=embedding_model.encode(chunk).astype("float32")
 
index=faiss.IndexFlatL2(384)
index.add(np.array(doc_model))
 
 
def faiss_reyrieve(query : str):
    query_v=embedding_model.encode([query]).astype('float32')
    d,idata=index.search(query_v,k=3)
    print("\n".join(chunk[i] for i in idata[0]))
    return "\n".join(chunk[i] for i in idata[0])
 
 
retriever_tool=FunctionTool(func=faiss_reyrieve)
 

root_agent=LlmAgent(
    name="AckoPolicyDocAgent",
    model="gemini-1.5-flash",
    description="Retrieve relevant chunks from the Acko Retail Health Policy PDF using a FAISS index",
    tools=[retriever_tool],
    instruction="""
    You are an expert insurance assistant. You must ALWAYS use the `retriever_tool` to retrieve relevant information from the document 'Policy-Wording-Acko-Retail-Health-Policy.pdf'.
    Never answer directly unless the `retriever_tool` is called.

    Typical questions may include:
    - What is covered under this health policy?
    - What are the exclusions?
    - What is the sum insured?
    - What is the claim process?
    - What are the waiting periods?

    Always follow these steps:
    1. Use `retriever_tool` to find relevant info from the PDF.
    2. Read the output from the tool.
    3. Then format a helpful, clear answer.

    If you don’t find the info, say “I couldn’t find it in the document.”
    """
)
 