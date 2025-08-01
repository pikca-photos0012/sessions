

from sentence_transformers import SentenceTransformer
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="https://3bc81ea2-1ee1-4669-892e-a9907c817399.us-west-2-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Tj2zIxV7zYWJBXcg0ZeUpqNSyfPBbqmrkYfDyydw6go",
)

collection_name = "insurance_data"

def qdrant_retrieve(query: str):
    query_vector = embedding_model.encode([query])[0].astype("float32")
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3,
        with_payload=True
    )
    chunks = [point.payload.get("chunk", "") for point in search_result]
    print("\n".join(chunks))
    return "\n".join(chunks)

retriever_tool = FunctionTool(func=qdrant_retrieve)

root_agent = LlmAgent(
    name="AckoPolicyDocAgent",
    model="gemini-1.5-flash",
    description="Retrieve relevant chunks from the Acko Retail Health Policy PDF using Qdrant",
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
 