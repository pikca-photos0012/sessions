from google.adk.agents import Agent
from google.adk.tools import google_search
 
 
root_agent=Agent(
    name='search_agent',
    description="Ask me anything! I will try to answer",
    instruction='Answer user questions to the best of your knowledge using google search content',
    model="gemini-1.5-flash",
    tools=[google_search]
)