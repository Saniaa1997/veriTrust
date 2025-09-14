import streamlit as st
from verifier import get_latest_articles
from utils import similarity_score

st.set_page_config(page_title="VeriTrust", page_icon="🕵️", layout="centered")
st.title("🕵️ VeriTrust: Real-Time Fake News Detector")

user_input = st.text_input("📰 Enter a news headline or article to verify:")

if user_input:
    with st.spinner("🔍 Verifying with real-time news data..."):
        articles = get_latest_articles()

        if not articles:
            st.error("⚠️ Could not fetch news headlines.")
        else:
            top_results = similarity_score(user_input, articles)[:5]
            top_score = top_results[0]["score"]

            st.markdown("### 📰 Top 5 Most Similar Real News Articles:")

            for i, result in enumerate(top_results, start=1):
                st.markdown(
                    f"**{i}.** [{result['title']}]({result['url']})  \n"
                    f"Similarity Score: `{result['score']:.2f}`"
                )

            if top_score >= 0.4:
                st.success("✅ This news is likely REAL based on recent headlines.")
            else:
                st.error("❌ This news might be FAKE or unverifiable.")
