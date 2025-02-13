import streamlit as st
import spacy
from random import sample

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Dictionary to temporarily store uploaded documents by session (not saved persistently)
session_state = st.session_state
if 'uploaded_documents' not in session_state:
    session_state.uploaded_documents = []

# Function to generate content ideas based on input
def generate_content_ideas(niche, topic):
    content_ideas = [
        (f"Harnessing {topic} for Smarter {niche} Management: Unlocking the Potential of Innovative Practices",
         "Explore how the latest advancements in AI and data analytics are transforming business management, offering new tools for enhanced decision-making and efficiency."),
        
        (f"The Future of {niche} and {topic}: Preparing Your Organization for an Evolving Landscape",
         "Examine the impact of emerging trends and technologies in this field, highlighting strategies for adapting to a future shaped by innovation and digital transformation."),
        
        (f"Navigating the {topic} Landscape: A Visual Guide to {topic} Applications Across {niche}",
         "Curate a visually engaging infographic or interactive experience that showcases current {topic} use cases, from virtual assistants to predictive analytics, to illustrate the impact across industries."),
        
        (f"Mastering the Art of {topic} in {niche}: Strategies to Gain a Competitive Edge",
         "Provide a detailed guide on integrating advanced {topic} techniques into {niche} practices, with tips for staying ahead of the competition."),
        
        (f"Exploring the Intersection of {topic} and {niche}: How It's Shaping Modern Trends",
         "Analyze the latest innovations at the intersection of {niche} and {topic}, with real-world examples that demonstrate their growing influence in the market.")
    ]
    return sample(content_ideas, 5)  # Return 5 unique ideas with descriptions

# Set page configuration
st.set_page_config(page_title="Content Idea Generator & Document Search", page_icon="📝")

# Custom CSS for background image
background_image_url = "https://www.istockphoto.com/photo/student-working-in-library-at-night-gm143071446-24422647"  # Change to your preferred image
# Custom CSS for background image and button styling
st.markdown(f"""
    <style>
    .stApp {{
        background: url("{background_image_url}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Custom styling for the Generate button */
    .stButton>button {{
        background-color: #e3f2fd;  /* Pale blue (default) */
        color: #000;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease, color 0.3s ease;
    }}

    .stButton>button:hover {{
        background-color: #90caf9;  /* Darker blue when hovered */
        color: #000;
    }}

    .stButton>button:active {{
        background-color: #1976d2 !important;  /* Deep blue when clicked */
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Content Idea Generation Section
st.header("Content Idea Generator")
niche = st.text_input("Niche", placeholder="e.g., Technology, Health, Marketing")
topic = st.text_input("Topic", placeholder="e.g., AI, Machine Learning, Social Media")

if st.button("Generate Content Ideas"):
    if niche and topic:
        ideas = generate_content_ideas(niche, topic)
        st.write("5 unique and creative content ideas related to the given niche and topic:")
        for i, (title, description) in enumerate(ideas, 1):
            st.markdown(f"""
                <div class="idea-box">
                    <div class="idea-title">Idea {i}: "{title}"</div>
                    <div class="idea-description">{description}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Please enter both a niche and a topic.")

# Document Upload and Search Section
st.header("Document Upload and Search")
uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Attempt to decode file content using UTF-8, falling back to ISO-8859-1 if necessary
        try:
            doc_content = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            try:
                doc_content = uploaded_file.read().decode("ISO-8859-1")
            except UnicodeDecodeError:
                st.error(f"Could not decode {uploaded_file.name}. Please upload a UTF-8 or ISO-8859-1 encoded file.")
                continue  # Skip this file if decoding fails
        
        session_state.uploaded_documents.append((uploaded_file.name, doc_content))
    st.success("Documents uploaded successfully.")

# Search field for finding uploaded documents based on niche and topic
st.subheader("Search for Documents by Niche and Topic")
search_niche = st.text_input("Search Niche", placeholder="e.g., Technology")
search_topic = st.text_input("Search Topic", placeholder="e.g., AI")

if st.button("Search Documents"):
    if search_niche and search_topic:
        found_documents = []
        for doc_name, doc_content in session_state.uploaded_documents:
            # Basic keyword matching to identify if the document contains the topic and niche
            if search_niche.lower() in doc_content.lower() and search_topic.lower() in doc_content.lower():
                found_documents.append((doc_name, doc_content[:300]))  # Display first 300 characters as preview
        
        if found_documents:
            st.write(f"Documents related to niche '{search_niche}' and topic '{search_topic}':")
            for doc_name, doc_preview in found_documents:
                st.markdown(f"<div class='doc-display'><strong>{doc_name}</strong><br>{doc_preview}...</div>", unsafe_allow_html=True)
        else:
            st.write(f"No documents found for niche '{search_niche}' and topic '{search_topic}'")
    else:
        st.write("Please enter both a search niche and a topic.")
