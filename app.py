import streamlit as st
from verifier import get_latest_articles
from utils import similarity_score
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="VeriTrust", page_icon="🛡️", layout="wide")

# Get base64 string for the background image
def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

try:
    base64_img = get_base64_image("img.jpg")
except FileNotFoundError:
    st.error("Error: 'img.jpg' not found in the project directory. Please check the file path.")
    base64_img = "" 

# --- Corrected CSS for Consistent Padding and Visibility ---
st.markdown(f"""
    <style>
        /* Apply background image to the entire app */
        .stApp {{
            background: url("data:image/jpeg;base64,{base64_img}") no-repeat center center fixed;
            background-size: cover;

        }}
        
        /* Ensure content is readable by applying a semi-transparent background to the main block */
        .main .block-container {{
            padding-top: 9rem;
            padding-bottom: 9rem;
            padding-left: 9rem;
            padding-right: 9rem;
            background-color: #ffffff
            background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent white overlay */
            border-radius: 12px;

        }}
        
        /* Hero section with a darker overlay to make text pop */
        .hero-section {{
            position: relative;
            width: 100%;
            height: 360px;
            background:  url('data:image/jpeg;base64,{base64_img}') no-repeat center center;
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            color: white;
            
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .hero-section h1 {{
            font-size: 3em;
            margin: 0;
            font-weight: bold; /* Make title bolder for better contrast */
        }}
        .hero-section p {{
            font-size: 1.25em;
            margin: 10px 0 0;
            font-weight: bold; /* Make subtitle bolder as well */
        }}

        /* General styling for inputs and cards */
        .stTextArea, .stTextInput, .stSlider {{
            background-color: #ffffff;
            margin: 10px 0 0;
            border-radius: 0px;
            font-color: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            use_column_width=True
        }}

        /* Make Streamlit's default headers and markdown text visible */
        h1, h2, h3, h4, h5, h6 {{
            color: #2E3A59;
            text-shadow: none; /* Remove text shadow that was clashing */
        }}
        p, .stMarkdown {{
            color: #444;
            
        }}

        /* Specific styling for the info/warning/error boxes */
        [data-testid="stText"] {{
            color: #333 !important;
        }}
    </style>
""", unsafe_allow_html=True)


# Hero section with a dark overlay to ensure text visibility
st.markdown(f"""
    <div class="hero-section">
        <h1>VeriTrust</h1>
        <p>Real-Time Location-Based Fake News Verification System</p>
    </div>
""", unsafe_allow_html=True)


# ------------------- Fragment: Intelligent Verification Engine -------------------
st.markdown("""
<div style="background-color:#f0f2f6; padding:20px 25px; border-radius:12px; margin-top:30px;">
    <h2 style="color:#2E3A59; font-size: 22px; margin-bottom: 10px;">🧠 Intelligent Verification Engine</h2>
    <p style="color:#444; font-size: 15px; line-height:1.6;">
        This engine uses AI-powered sentence embeddings to check how closely a news article matches with recent news headlines from reliable sources.
        The analysis is done based on the location you specify, making the verification context-aware and region-specific.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------- News Input Form (Nested Containers) -------------------

with st.container(): # Parent container for the form
    with st.container(): # Child container for the form
        st.markdown("#### 📥 News Input")
        with st.form(key="veriform"):
            user_input = st.text_area(
            "Enter news headline or content",
            placeholder="e.g., Government announces new policy on electric vehicles...",
            height=120
            )

            location = st.text_input(
            "Enter location (City or Country)",
            placeholder="e.g., New York, India, London..."
            )

            threshold = st.slider(
            "Verification strictness (similarity threshold)", 
            0.0, 1.0, 0.4, 0.05
            )

            submitted = st.form_submit_button("🔍 Verify News", use_container_width=True)

# ------------------- Result Section -------------------
if submitted and user_input and location:
    with st.spinner("🔬 Verifying news using real-time data..."):
        articles = get_latest_articles(location=location, limit=10)
        results = similarity_score(user_input, articles, top_n=5)

    if results:
        top_score = results[0]["score"]
        verdict = "Likely Real ✅" if top_score >= threshold else "Likely Fake or Unverified ❌"
        verdict_color = "#00C853" if top_score >= threshold else "#D32F2F"

        # Final Verdict card
        st.markdown(f"""
            <div style="border: 2px solid {verdict_color}; border-radius: 10px; padding: 20px; margin-top: 20px;">
                <h3 style="color: {verdict_color};">Final Verdict</h3>
                <p style="font-size: 18px; font-weight: 500; color: #333;">{verdict}</p>
            </div>
        """, unsafe_allow_html=True)

        # Similar Articles
        st.markdown("### 🔗 Most Similar Articles")
        for i, result in enumerate(results, start=1):
            card_color = "#F1F3F4" if result["score"] < threshold else "#E8F5E9"
            st.markdown(f"""
                <div style="background-color: {card_color}; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <strong>{i}. <a href="{result['url']}" target="_blank" style="color: #0072FF;">{result['title']}</a></strong><br>
                    <span style="font-size: 14px; color: #555;">Similarity Score: {result['score']:.2f}</span>
                </div>
            """, unsafe_allow_html=True)

        # Graph of similarity scores
        st.markdown("### 📊 Similarity Score Graph")
        df = pd.DataFrame(results)
        fig = px.bar(df, x='title', y='score', color='score', title="Top Article Similarity Scores")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No similar articles found. Try a broader region or headline.")

elif submitted and not user_input:
    st.error("Please enter a news headline or content.")

elif submitted and not location:
    st.error("Please specify a location.")

# ------------------- Footer -------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align:center; font-size: 14px; color: #ffff;">
        VeriTrust © 2025 — Built with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)