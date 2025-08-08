

from sentence_transformers import SentenceTransformer
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import os
from dotenv import load_dotenv
from .tools.openai_gaurdrails import openai_moderation_guardrail

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
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
    name="compliance_moderated_bot",
    model="gemini-1.5-flash",
    instruction="""
        you are a helpful HR compliance assistant. Always first check the query using openai_moderation_guardrail and answer policy related questions using retriever_tool.

        Typical questions may include:
            - What is covered under this health policy?
            - What are the exclusions?
            - What is the sum insured?
            - What is the claim process?
            - What are the waiting periods?

        Always follow these steps:
        1. Use openai_moderation_guardrail to check the query for unsafe content before any other action.
        2. Must use openai_moderation_guardrail to check for unsafe content in the query before answering.
        3. Mention the nature of the query based on the response from openai_moderation_guardrail.
        4. If the query is flagged, respond with a message indicating that the query has been flagged by safety filters and suggest rephrasing or contacting HR directly.
        5. If the query is allowed, use retriever_tool to find relevant info from the document and answer the question.
        6. If you don’t find the info, say “I couldn’t find it in the document.”

""",
    tools=[openai_moderation_guardrail, retriever_tool]
)
 