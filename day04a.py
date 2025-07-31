
import streamlit as st

# Set Streamlit page config for dark/neon theme
st.set_page_config(
	page_title="Neon Semantic Search App",
	page_icon="🔎",
	layout="centered",
	initial_sidebar_state="auto"
)

# Inject custom CSS for neon/dark theme and legible input labels
st.markdown(
	"""
	<style>
	body, .stApp {
		background-color: #18122B !important;
		color: #F0F0F0 !important;
	}
	.stTextInput > div > div > input, .stTextArea textarea {
		background: #232946 !important;
		color: #39FF14 !important;
		border: 1.5px solid #39FF14 !important;
		font-weight: bold;
	}
	/* Make text area and input labels neon and legible */
	label, .stTextInput label, .stTextArea label {
		color: #39FF14 !important;
		font-weight: bold !important;
		text-shadow: 0 0 8px #00FFFF, 0 0 2px #39FF14;
		font-size: 1.1rem !important;
	}
	.stButton > button {
		background: linear-gradient(90deg, #39FF14 0%, #00FFFF 100%) !important;
		color: #18122B !important;
		font-weight: bold;
		border-radius: 8px;
		border: none;
		box-shadow: 0 0 10px #39FF14, 0 0 20px #00FFFF;
		transition: 0.2s;
	}
	.stButton > button:hover {
		background: linear-gradient(90deg, #00FFFF 0%, #39FF14 100%) !important;
		color: #232946 !important;
		box-shadow: 0 0 20px #00FFFF, 0 0 40px #39FF14;
	}
	.stTextArea textarea:focus, .stTextInput input:focus {
		outline: 2px solid #00FFFF !important;
		box-shadow: 0 0 10px #00FFFF;
	}
	.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
		color: #39FF14 !important;
		text-shadow: 0 0 10px #00FFFF;
	}
	.stNumberInput input {
		background: #232946 !important;
		color: #39FF14 !important;
		border: 1.5px solid #39FF14 !important;
		font-weight: bold;
	}
	.stAlert {
		background: #232946 !important;
		color: #FF00FF !important;
		border: 2px solid #FF00FF !important;
	}
	</style>
	""",
	unsafe_allow_html=True
)
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

st.title("Document Semantic Search App")


st.write("Enter your documents below (one per line):")
default_docs = """
AI is transforming the world.
Generative AI models are powerful.
Data science uses machine learning.
AI can help businesses grow.
Machine learning improves predictions.
My laptop has 16 GB RAM.
I am using iPhone.
I am using Apple and Asus laptop.
My laptop is not working.
The weather is sunny today.
I love playing football.
Python is a popular programming language.
The stock market is volatile.
She enjoys reading science fiction novels.
The new restaurant serves Italian food.
My favorite color is blue.
He is learning to play the guitar.
The train was delayed by two hours.
I need to buy groceries.
The movie was very entertaining.
She has a pet dog named Max.
The conference starts at 9 AM.
I am planning a trip to Japan.
The book was better than the movie.
He works as a software engineer.
The cake tastes delicious.
I forgot my umbrella at home.
The museum has ancient artifacts.
She is preparing for her exams.
The car needs an oil change.
I enjoy hiking in the mountains.
The internet connection is slow.
He bought a new bicycle.
The flowers are blooming in spring.
I am allergic to peanuts.
The team won the championship.
She is writing a research paper.
The coffee shop is crowded.
I have a meeting at noon.
The cat is sleeping on the sofa.
He is watching a documentary.
The pizza delivery was late.
I am learning French online.
The festival was colorful and lively.
She is baking cookies for the party.
The river flows through the city.
I need to charge my phone.
The library is open until 8 PM.
He is painting a landscape.
The bus stop is near my house.
I am listening to classical music.
The garden has many roses.
She is practicing yoga every morning.
The laptop battery is low.
I am attending a webinar.
The bakery sells fresh bread.
He is fixing the broken chair.
The mountain view is breathtaking.
I am organizing my desk.
The dog barked all night.
She is learning to swim.
The restaurant is fully booked.
I am reading a mystery novel.
The printer is out of ink.
He is jogging in the park.
The soup is too salty.
I am updating my resume.
The phone screen is cracked.
She is designing a website.
The air conditioner is not working.
I am making a cup of tea.
The children are playing outside.
He is building a treehouse.
The shoes are on sale.
I am watching a comedy show.
The fridge is empty.
She is planting tomatoes in the garden.
The exam was difficult.
I am learning to cook Indian food.
The lamp is flickering.
He is driving to the airport.
The painting is very old.
I am writing a letter to my friend.
The bakery is famous for its cakes.
She is attending an online class.
The dog chased the squirrel.
I am going for a walk.
The rain is pouring heavily.
He is playing chess with his brother.
The soup needs more pepper.
I am cleaning my room.
The movie starts at 7 PM.
She is knitting a scarf.
The car alarm went off.
I am learning about machine learning.
The teacher gave us homework.
He is reading the newspaper.
The window is open.
I am making breakfast.
The festival will last three days.
She is drawing a portrait.
The computer crashed unexpectedly.
I am searching for my keys.
The music is too loud.
He is watering the plants.
The store closes at 10 PM.
I am writing code in Python.
"""
docs_input = st.text_area("Documents", value=default_docs.strip(), height=400)

query = st.text_input("Enter your query:", value="what is RAM size of my laptop")
k = st.number_input("Number of relevant documents to retrieve", min_value=1, max_value=10, value=3)

if st.button("Search"):
	documents = [doc.strip() for doc in docs_input.strip().split('\n') if doc.strip()]
	if not documents:
		st.warning("Please enter at least one document.")
	elif not query.strip():
		st.warning("Please enter a query.")
	else:
		model = SentenceTransformer('all-MiniLM-L6-v2')
		document_embeddings = model.encode(documents)
		embedding_dim = document_embeddings.shape[1]
		index = faiss.IndexFlatL2(embedding_dim)
		index.add(np.array(document_embeddings))
		query_embedding = model.encode([query])
		D, I = index.search(np.array(query_embedding), int(k))
		st.subheader("Top relevant documents:")
		for idx in I[0]:
			st.write(f"- {documents[idx]}")
