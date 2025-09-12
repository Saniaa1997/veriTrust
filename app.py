import streamlit as st
from verifier import verify_news

st.title("📰 VeriTrust - Fake News Verifier")
st.subheader("Check if a news headline is real or fake using AI 🔍")

input_text = st.text_input("Enter a news headline:")

if st.button("Verify"):
    if input_text:
        label, scores, articles = verify_news(input_text)
        st.write(f"### Verdict: {label}")
 
