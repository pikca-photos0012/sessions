from PyPDF2 import PdfReader
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, PointStruct

import uuid


data=r"C:\Users\labuser\Downloads\sessions\Policy-Wording-Acko-Retail-Health-Policy.pdf"

reader=PdfReader(data)
raw_text="\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
# print(raw_text)

embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
 
 
def create_chunk(text,chunk_size=1000,overlap=200):
    chunk=[]
    start=0
    while start<len(text):
        end=start +chunk_size
        chunk.append(text[start:end])
        start+=chunk_size-overlap
    return chunk
 
chunk_data=create_chunk(raw_text)
 
 
doc_model=embedding_model.encode(chunk_data).astype("float32")

qdrant_client = QdrantClient(
    url="https://3bc81ea2-1ee1-4669-892e-a9907c817399.us-west-2-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Tj2zIxV7zYWJBXcg0ZeUpqNSyfPBbqmrkYfDyydw6go",
)

collection_name = "insurance_data"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    )
)

points = [
    PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={"chunk": chunk_}
    )
    for chunk_, embedding in zip(chunk_data, doc_model)
]

qdrant_client.upsert(
    collection_name=collection_name,
    points=points
)
