import streamlit as st
from verifier import verify_news

st.set_page_config(
    page_title="VeriTrust - Fake News Verifier",
    page_icon="🕵️",
    layout="centered"
)

st.title("🕵️ VeriTrust - AI Fake News Verifier")
st.markdown("Enter a news headline or short news snippet below to verify its trustworthiness.")

# User input
user_input = st.text_area("📝 Enter news headline or snippet:", height=100)

# Verify button
if st.button("✅ Verify"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a valid news snippet to proceed.")
    else:
        label, scores, articles = verify_news(user_input)

        # Display result
        st.markdown(f"### ✅ Prediction: `{label}`")

        if articles:
            st.markdown("### 🔍 Top Matching Articles:")
            for i, article in enumerate(articles):
                st.markdown(f"**{i+1}.** {article}  \nSimilarity Score: `{scores[i]:.2f}`")

        st.markdown("### 🙋 Was this result helpful?")
        col1, col2 = st.columns(2)
        with col1:
            st.button("👍 Yes")
        with col2:
            st.button("👎 No")
