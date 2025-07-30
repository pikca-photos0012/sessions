from google import genai
import streamlit as st
import os
os.environ["GEMINI_API_KEY"]="AIzaSyAPHS04lFQvJjhR1N8dnETCpaQwte83yUA"
 
 
clinet=genai.Client()
 
st.title("my chat application")
 
prompt=st.text_input("enter your question")
 
 
if st.button("Enter"):
    res=clinet.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    st.write(res.text)
    