from google import genai
import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
 
 
os.environ["GEMINI_API_KEY"]="AIzaSyAPHS04lFQvJjhR1N8dnETCpaQwte83yUA"
clinet=genai.Client()

# print([i for i in clinet.models.list()])



# --- Custom CSS for dark mode and professional look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, .stApp {
        background: linear-gradient(120deg, #181c24 0%, #232a36 100%) !important;
        color: #e0e6ed !important;
        font-family: 'Inter', sans-serif;
    }
    .fade-in-image {
        opacity: 0;
        animation: fadeIn 1.2s ease-in-out forwards;
        box-shadow: 0 2px 12px #10131a;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #353b48;
        background: #232a36;
        color: #e0e6ed;
        padding: 10px 14px;
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input:focus {
        border: 1.5px solid #4f8cff;
        outline: none;
    }
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(90deg, #4f8cff 0%, #2563eb 100%);
        color: #fff;
        font-weight: 600;
        font-size: 1.08rem;
        padding: 8px 24px;
        border: none;
        box-shadow: 0 2px 8px #10131a44;
        transition: background 0.2s, box-shadow 0.2s;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #4f8cff 100%);
        box-shadow: 0 4px 16px #10131a88;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #e0e6ed;
    }
    .stSpinner {
        color: #4f8cff !important;
    }
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<h1 style="text-align:center;font-weight:600;font-size:2.5rem;letter-spacing:-1px;">✨ AI Image Chat <span style='color:#4f8cff;'>Pro</span> ✨</h1>
<p style="text-align:center;font-size:1.15rem;color:#b0b8c1;margin-bottom:2.5rem;">Ask a question and get AI-generated images with a smooth, professional dark mode experience.</p>
""", unsafe_allow_html=True)

prompt = st.text_input("Enter your question")

if st.button("Enter"):
    with st.spinner("Generating images, please wait..."):
        res = clinet.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt
        )
    if hasattr(res, "generated_images") and res.generated_images:
        cols = st.columns(2)
        for idx, img in enumerate(res.generated_images[:4]):
            if hasattr(img.image, "image_bytes") and img.image.image_bytes:
                try:
                    image = Image.open(BytesIO(img.image.image_bytes))
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    img_html = f'<img src="data:image/png;base64,{img_b64}" class="fade-in-image" style="width:100%;margin-bottom:16px;border-radius:12px;box-shadow:0 2px 8px #b0b8c1;"/>'
                    with cols[idx % 2]:
                        st.markdown(img_html, unsafe_allow_html=True)
                except Exception:
                    st.write("Could not display image from image_bytes.")
            else:
                st.write("Unsupported image format.")
    else:
        st.write("No image generated.")
    