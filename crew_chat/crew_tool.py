
import os
import requests
import streamlit as st
from dotenv import load_dotenv

# CrewAI imports
from crewai import Agent, Task, Crew
from crewai.tools import tool

load_dotenv()

@tool
def evaluate_expression(expr: str):
    """Evaluates a mathematical expression using MathJS API."""
    api_url = "https://api.mathjs.org/v4/"
    response = requests.get(api_url, params={"expr": expr})
    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"API Error : {response.status_code}  {response.text}"
    
@tool
def brave_search(query: str):
    """Searches the web using Brave Search API and returns the top 3 results."""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        return "Error: BRAVE_API_KEY not set in environment."
    if not query or not query.strip():
        return "Error: Query is empty."
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    params = {"q": query, "count": 3}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)  # For debugging
        result = data.get("web", {}).get("results", [])
        summary = "\n\n".join(f"{r['title']}\n{r['url']}" for r in result)
        return summary if summary else "No result found"
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        return f"Error: {response.status_code}\nDetails: {error_detail}"


st.title("CrewAI Chat Agent")
user_query = st.text_input("Enter your question")


# The agent can now use both brave_search and evaluate_expression
chat_agent = Agent(
    role="Helpful Assistant",
    goal="Use Brave Search for web queries and MathJS for math expressions. Decide which tool to use based on the user's question.",
    backstory="You are a web-connected assistant using Brave Search for general queries and MathJS for math calculations.",
    tools=[brave_search, evaluate_expression]
)

if st.button("Ask Agent") and user_query:
    task = Task(
        description=f"Answer the user question: '{user_query}'",
        expected_output="A clear, concise explanation of user question",
        agent=chat_agent
    )

    crew = Crew(
        agents=[chat_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    st.success("Agent Answer")
    st.markdown(result)
    print("\n\n Final Answer:\n", result)