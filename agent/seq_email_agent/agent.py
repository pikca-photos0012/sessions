import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
import requests
 
 
 
import smtplib
from email.mime.text import MIMEText
 
 
 
 
 
def send_email (data: dict):
    print(data)
    send_email = "pikca.photos0012@gmail.com"
    passw = os.getenv("APP_PASSWORD")  # Use your Gmail App Password here
 
    msg=data['body']
    message=MIMEText(msg)
    message["Subject"]= data["subject"]
    message['From']=send_email
    message['To']=data["to"]
 
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(send_email,passw)
        server.send_message(message)
        print("email sent")
    return "email sent"
 
send_email=FunctionTool(send_email)
 
root_agent= LlmAgent(
    name="generate_email",
    model='gemini-1.5-flash',
    tools=[send_email],
    instruction="""
        You are a professional assistant. Based on the user's message, write a professional elaborate email with:
        - 'subject'
        - 'body'
        - 'recipient' (email to send to)
 
        The email should be clear, elaborate, and professional.
        if the user missed any information like sender name, ask them to provide it.
        Use the following format to return the email data:
        Return as a JSON like:
        {
        "subject": "...",
        "body": "...",
        "to": "abc@example.com"
        }    after that call   `send_email` tool to send email to customer
        always call tool `send_email in the last`""",
    description="agent who prepare email based on user message",
 
)
 