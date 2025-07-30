from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool

import requests

def evaluate_expression(expr: str):
    api_url = "https://api.mathjs.org/v4/"
    response = requests.get(api_url, params={"expr": expr})
    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"API Error : {response.status_code}  {response.text}"

cal_tool = FunctionTool(evaluate_expression)

root_agent=Agent(
    name='search_agent',
    description="Assistant that solves mathematical expressions.",
    instruction='Use the calculate tool to evaluate expressions. If invalid, ask for clarification.',
    model="gemini-1.5-flash",
    tools=[cal_tool]
)