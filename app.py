import streamlit as st
from verifier import verify_news

st.title("📰 VeriTrust - Fake News Verifier")
st.subheader("Check if a news headline is real or fake using AI 🔍")

input_text = st.text_input("Enter a news headline:")

if st.button("Verify"):
    if not input_text.strip():
        st.warning("⚠️ Please enter a news headline before verifying.")
    else:
        try:
            label, scores, articles = verify_news(input_text)
            
            st.write(f"### Verdict: {label}")

            if articles:
                st.write("#### Related News Articles:")
                for i, (article, score) in enumerate(zip(articles, scores)):
                    st.markdown(f"**{i+1}.** {article}  \n_Similarity: {score:.2f}_")
            else:
                st.info("No related articles found. Please try a different headline.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

