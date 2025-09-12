import streamlit as st
from verifier import verify_news

st.title("📰 VeriTrust - Fake News Verifier")
st.subheader("Check if a news headline is real or fake using AI 🔍")

input_text = st.text_input("Enter a news headline:")

if st.button("Verify"):
    if input_text:
        label, scores, articles = verify_news(input_text)
        st.write(f"### Verdict: {label}")
        st.write("#### Related News Articles:")
        for i, (article, score) in enumerate(zip(articles, scores)):
            st.markdown(f"**{i+1}.** {article}  \n_Similarity: {score:.2f}_")

