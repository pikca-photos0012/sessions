from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool


import asyncio
import requests


STOCK_DATA={
    "APPL":45.456,
    "GOOG":767.67,
    "TESLA":57.67,
    "CEAT":909
}

def get_stock_price(mydata: str):
    mydata = mydata.upper()
    if mydata in STOCK_DATA:
        return {"result": f"The current price {mydata} is ${STOCK_DATA[mydata]}"}
    return {"result": f"No data found for {mydata}"}

stock_tool = FunctionTool(get_stock_price)

def evaluate_expression(expr: str):
    api_url = "https://api.mathjs.org/v4/"
    response = requests.get(api_url, params={"expr": expr})
    if response.status_code == 200:
        return {"result": response.text.strip()}
    else:
        return {"result": f"API Error : {response.status_code}  {response.text}"}

cal_tool = FunctionTool(evaluate_expression)


# Define a sub-agent for search
search_agent = Agent(
    name='sub_search_agent',
    description="Agent dedicated to searching Google.",
    instruction='Use the google_search tool for all search queries.',
    model="gemini-1.5-flash",
    tools=[google_search]
)

async def call_search_agent(query: str):
    """Calls the sub_search_agent to perform a search asynchronously."""
    result_gen = search_agent.run_live(query)
    output = ""
    async for chunk in result_gen:
        print(f"search_agent chunk: {chunk}")
        output += str(chunk)
    return {"result": output}

search_tool = FunctionTool(call_search_agent)

root_agent = Agent(
    name='root_agent',
    description="Root assistant that solves mathematical expressions, retrieves stock values from a local reference list, and delegates search to a sub-agent.",
    instruction='Use the calculate tool to evaluate mathematical expressions. Use the search_tool for general queries. Use the stock_tool to get the latest stock value of a company from the local reference list. If input is invalid, ask for clarification.',
    model="gemini-1.5-flash",
    tools=[cal_tool, search_tool, stock_tool]
    # tools=[cal_tool, google_search]
)