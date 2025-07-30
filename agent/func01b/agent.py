from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool


import asyncio
import requests
import json




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

# Function to get response from the local server (similar to screenshot)
def get_local_server_response(payload: str):
    print(payload)
    url = "http://localhost:5000"
    # data = json.loads(payload)
    data = payload
    response = requests.post('http://127.0.0.1:5000/', json=data)
    return str(response.content)

predict_energy_output_tool = FunctionTool(get_local_server_response)

root_agent = Agent(
    name='root_agent',
    description="Agent that calculate math expression and restun output",
    instruction=(
        "USe this calculation tool when user give math question or ask to solve math problem"
        "Use the Stockdata tool only when user ask question related to stock price "
        """Use predict energy output tool when user ask to predict eneergy poutput based on\n"
        "temperature exhaust_vacuum ambient_pressure relative_humidity\n"
        "and make sure convert into brlow format\n"
            {'temperature': 1.0, 'exhaust_vacuum': 2.0, 'ambient_pressure': 3.0, 'relative_humidity': 4.0}
        while sending request here data is key and other into value of temperature vaccum pressure humidity"""
    ),
    model="gemini-1.5-flash",
    tools=[cal_tool, stock_tool, predict_energy_output_tool]
    # tools=[cal_tool, google_search]
)