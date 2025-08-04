
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
 
 
load_dotenv()
 
llm=ChatOpenAI(model="gpt-3.5-turbo")
 
 
def user_input(state:dict):
    user_msg=input("You: ")
    if user_msg.strip().lower()=="exit()":
        print("Goodbye !!")
        exit()
    state["history"].append(HumanMessage(user_msg))
    return state
 
 
def llm_node(state:dict):
    response=llm.invoke(state["history"])
    print("Bot: ",response.content)
    state["history"].append(response)
    return state
 
graph=StateGraph(dict)
graph.add_node("user_input",user_input)
graph.add_node("llm_response",llm_node)
graph.set_entry_point("user_input")
graph.add_edge("user_input","llm_response")
graph.add_edge("llm_response","user_input")
 
 
app=graph.compile()
state={'history':[]}
 
while True:
    state = app.invoke(state)
 
 