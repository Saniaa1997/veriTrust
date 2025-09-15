import streamlit as st
from verifier import get_latest_articles
from utils import similarity_score
from PIL import Image
from pathlib import Path

# --- Config ---
st.set_page_config(page_title="VeriTrust", page_icon="🛡️", layout="centered")

# --- Load image ---
image_path = Path("veritrust_header.jpg")
if image_path.exists():
    st.image(Image.open(image_path), use_column_width=True)

# --- Header Section ---
with st.container():
    st.markdown("""
        <div style="text-align: center; margin-top: -30px;">
            <h1 style="font-size: 3em; color: #2E3A59; margin-bottom: 0;">VeriTrust</h1>
            <p style="font-size: 1.25em; color: #5F6A84; font-weight: 500;">Real-Time Location-Based Fake News Verification System</p>
        </div>
        """, unsafe_allow_html=True)

# --- Body Layout ---
with st.container():
    st.markdown("## 🧠 Intelligent Verification Engine")
    st.markdown("""
    <p style="color:#444; font-size: 16px;">
        Use cutting-edge AI to verify news articles in real-time, powered by recent trustworthy news data based on the region you choose.
    </p>
    """, unsafe_allow_html=True)

    # --- Input Card ---
    with st.container():
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

            threshold = st.slider("Verification strictness (similarity threshold)", 0.0, 1.0, 0.4, 0.05)

            submitted = st.form_submit_button("🔍 Verify News", use_container_width=True)

    # --- Output Logic ---
    if submitted and user_input and location:
        with st.spinner("🔬 Verifying news using real-time data..."):
            articles = get_latest_articles(location=location,limit=10)
            results = similarity_score(user_input, articles, top_n=5)

        if results:
            top_score = results[0]["score"]
            verdict_color = "#00C853" if top_score >= threshold else "#D32F2F"
            verdict_text = "Likely Real ✅" if top_score >= threshold else "Likely Fake or Unverified ❌"

            # --- Verdict Card ---
            st.markdown(f"""
                <div style="border: 2px solid {verdict_color}; border-radius: 10px; padding: 20px; margin-top: 20px;">
                    <h3 style="color: {verdict_color};">Final Verdict</h3>
                    <p style="font-size: 18px; font-weight: 500; color: #333;">{verdict_text}</p>
                </div>
            """, unsafe_allow_html=True)

            # --- Results Cards ---
            st.markdown("### 🔗 Most Similar Articles")
            for i, result in enumerate(results, start=1):
                card_color = "#F1F3F4" if result["score"] < threshold else "#E8F5E9"
                st.markdown(f"""
                    <div style="background-color: {card_color}; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                        <strong>{i}. <a href="{result['url']}" target="_blank" style="color: #0072FF;">{result['title']}</a></strong><br>
                        <span style="font-size: 14px; color: #555;">Similarity Score: {result['score']:.2f}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No similar articles found. Try a broader region or headline.")

    elif submitted and not user_input:
        st.error("Please enter a news headline or content.")

    elif submitted and not location:
        st.error("Please specify a location.")
