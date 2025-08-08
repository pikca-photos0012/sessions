import os
import requests
from google.adk.tools import FunctionTool
 
@FunctionTool
def openai_moderation_guardrail(query:str):
    """
    open ai guradrail model to check unsafe content
    """
 
    openai_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {openai_key}"}
    # System prompt for safety and compliance
    system_prompt = (
        "You are a safety and domain compliance checker for an AI assistant.\n"
        "This assistant only answers questions that are:\n"
        "1. SAFE (no hate, violence, abuse, threats, self-harm, sexual content, or harassment)\n\n"
        "Classify the user query below as:\n"
        "- 'Query allowed' if it is safe and on-topic\n"
        "- 'Blocked: Unsafe' if it is toxic, abusive, threatening, or offensive\n"
    )
    user_prompt = f"User query: {query}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={**headers, "Content-Type": "application/json"},
        json=data,
        timeout=10
    )
    print("OpenAI Chat Completion API response:", response.text)
    result = response.json()
    content = result["choices"][0]["message"]["content"].strip().lower()
    if "blocked" in content or "unsafe" in content:
        return "Blocked: Unsafe - this query was flagged by safety filters, please rephrase or contact HR directly."
    return "Query allowed"
 