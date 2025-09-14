import streamlit as st
from verifier import get_latest_headlines
from utils import similarity_score

st.set_page_config(page_title="VeriTrust", page_icon="🕵️", layout="centered")
st.title("🕵️ VeriTrust: Real-Time Fake News Detector")

user_input = st.text_input("📰 Enter a news headline or article to verify:")

if user_input:
    with st.spinner("🔍 Verifying with real-time news data..."):
        real_articles = get_latest_headlines()

        if not real_articles:
            st.error("⚠️ Could not fetch headlines. Please check your API key or try again later.")
        else:
            scores = similarity_score(user_input, real_articles)
            max_score = max(scores)
            most_similar = real_articles[scores.argmax()]

            st.markdown("### 📰 Most Similar Real News:")
            st.info(most_similar)

            st.markdown(f"### 📊 Similarity Score: `{max_score:.2f}`")

            if max_score >= 0.35:
                st.success("✅ This news is likely REAL based on recent headlines.")
            else:
                st.error("❌ This news might be FAKE or not supported by recent headlines.")
