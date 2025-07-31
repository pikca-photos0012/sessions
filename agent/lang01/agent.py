from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.tools import FunctionTool
 
 
 
 
agent1=LlmAgent(
    name="Translator",
    model="gemini-1.5-flash",
    instruction="""
    Act as a professional translator who know mutiple language
    and convert english into tamil based on user request
    """,
    output_key="language_data"
    )
 
agent2=LlmAgent(
    name="summarizer",
    model="gemini-1.5-flash",
    instruction="""
    Act as a professional expert who summarize content into
    2 bullet point without missing context
    """,
    output_key="summary_data"
    )
 
agent3=LlmAgent(
    name="NER",
    model="gemini-1.5-flash",
    instruction="""
    Act as a professional expert who perfron NER and identify entity
    on user pr customer data like organization, name  or place like
    """,
    output_key="ner_data"
    )
 
 
root_agent=ParallelAgent(
    name="piprline",
    sub_agents=[agent1,agent2,agent3],
    description="agent who follow operation by running into parallel way different task"
)
 
 