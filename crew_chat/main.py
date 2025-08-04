import streamlit as st
import streamlit.components.v1 as components
from crewai import Agent, Task, Crew
from dotenv import load_dotenv




# Set Streamlit dark theme via config
st.set_page_config(
    page_title="CrewAI Q&A Assistant",
    layout="centered",
    initial_sidebar_state="auto"
)

# Inject improved dark theme CSS for all widgets
dark_css = """
<style>
body, .main, .block-container, .stApp {
    background: #181818 !important;
    color: #e0e0e0 !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #e0e0e0 !important;
}
.stTextInput>div>input, .stTextArea textarea {
    background: #222 !important;
    color: #e0e0e0 !important;
    border: 1px solid #444 !important;
}
.stTextInput label, .stTextArea label {
    color: #e0e0e0 !important;
    font-weight: bold;
    font-size: 1.1em;
}
.stButton>button {
    background: #444 !important;
    color: #e0e0e0 !important;
    border: none !important;
    font-weight: bold;
    transition: 0.2s;
}
.stButton>button:hover {
    background: #666 !important;
    color: #fff !important;
}
.stSuccess, .stMarkdown, .stSubheader, .stExpander {
    background: #222 !important;
    color: #e0e0e0 !important;
    border-radius: 8px;
    padding: 8px;
}
.stCodeBlock, .stCode {
    background: #181818 !important;
    color: #e0e0e0 !important;
    border: 1px solid #444 !important;
}
.stJson, .stDataFrame, .stTable {
    background: #222 !important;
    color: #e0e0e0 !important;
}
.stSelectbox>div>div {
    background: #222 !important;
    color: #e0e0e0 !important;
}
.stRadio>div>label {
    color: #e0e0e0 !important;
}
.stSlider>div {
    background: #222 !important;
    color: #e0e0e0 !important;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

st.title("CrewAI Q&A Assistant")
st.write("<span style='color:#e0e0e0;font-size:18px;'>Ask any question and get a clear, concise answer.</span>", unsafe_allow_html=True)

user_question = st.text_input("Enter your question:", "Can you compare Azure AWS GCP and Databricks Gen AI service and offering?")

if st.button("Get Answer"):
    chat_agent = Agent(
        role="Helpful Assistant",
        goal="Assist user by answering question clearly",
        backstory="You are a friendly assistant who helps users with everyday queries."
    )

    task = Task(
        description=f"Answer the user question: {user_question}",
        expected_output="A clear, concise explanation of user question",
        agent=chat_agent
    )

    crew = Crew(
        agents=[chat_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    st.success("Final Answer:")
    # Format output for result dict
    if isinstance(result, dict):
        # Show main answer as markdown in its own section
        if "raw" in result and result["raw"]:
            st.subheader("📝 Answer")
            st.markdown(result["raw"])

        # Show all other fields at the bottom
        st.markdown("---")
        st.subheader("🔍 Details")
        if "tasks_output" in result and result["tasks_output"]:
            with st.expander("Show Task Output"):
                for i, task_output in enumerate(result["tasks_output"], 1):
                    st.markdown(f"**Task {i}:**\n{task_output}")
        if "token_usage" in result and result["token_usage"]:
            st.markdown("**Token Usage:**")
            st.code(result["token_usage"], language="text")
        if "json_dict" in result and result["json_dict"]:
            st.markdown("**JSON Output:**")
            st.json(result["json_dict"])
    else:
        st.markdown(result)
        st.write(result)

 
 

