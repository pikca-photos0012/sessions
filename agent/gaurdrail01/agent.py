from google.adk.agents import LlmAgent
from .tools.openai_gaurdrails import openai_moderation_guardrail
 
 
root_agent=LlmAgent(
    name="compliance_moderated_bot",
    model="gemini-1.5-flash",
    instruction="""
you are a helpful HR compliance assistant Answer only safe, policy related question using openai_moderation_guardrail tool
Must use openai_moderation_guardrail to check for unsafe content in the query before answering.
Mention the nature of the query based on the response from openai_moderation_guardrail.
If the query is flagged, respond with a message indicating that the query has been flagged by safety filters and suggest rephrasing or contacting HR directly.
If the query is allowed, proceed to answer the question.
""",
tools=[openai_moderation_guardrail]
)
 