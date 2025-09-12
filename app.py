import streamlit as st
from verifier import verify_news
if "history" not in st.session_state:
    st.session_state.history = []


st.title("📰 VeriTrust - Fake News Verifier")
st.subheader("Check if a news headline is real or fake using AI 🔍")

input_text = st.text_input("Enter a news headline:")

if st.button("Verify"):
    if not input_text.strip():
        st.warning("⚠️ Please enter a news headline before verifying.")
    else:
        try:
            with st.spinner("🔎 Verifying..."):
                label, scores, articles = verify_news(input_text)

            
            if label == "Likely True":
                 st.success("✅ Verdict: Likely True")
            elif label == "Likely False":
                st.error("❌ Verdict: Likely False")
            else:
                st.warning("⚠️ Verdict: Needs Verification")


            if articles:
                st.write("#### Related News Articles:")
                for i, (article, score) in enumerate(zip(articles, scores)):
                    st.markdown(f"**{i+1}.** {article}  \n_Similarity: {score:.2f}_")
            else:
                st.info("No related articles found. Please try a different headline.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
st.session_state.history.append((input_text, label))

st.markdown("---")
st.markdown("Built with ❤️ during the Git Sprint Contest")
st.caption("Powered by NewsAPI and AI-based similarity scoring")
if st.session_state.history:
    st.markdown("### 🔁 Past Verifications")
    for i, (text, verdict) in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"{i}. _{text}_ → **{verdict}**")
