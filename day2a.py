from google import genai
import os
os.environ["GEMINI_API_KEY"]="AIzaSyAPHS04lFQvJjhR1N8dnETCpaQwte83yUA"
clinet=genai.Client()
res=clinet.models.generate_content(
    model="gemini-2.5-flash",
    contents="explain google cloud service in 10 bullet point related to gen ai and compare with aws bedrock"
)
print(res.text)