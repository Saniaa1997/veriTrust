# VeriTrust - AI-Based Fake News Verifier 
# 📰 VeriTrust – Your Friendly Fake News Verifier 🕵️‍♀️

Hi! 👋 This is **VeriTrust**, a simple and smart tool that helps you figure out if a news headline is real, fake, or needs a closer look — in just a few seconds.

Built as part of a Git-based coding sprint, this project focuses on clear version control, clean coding practices, and solving a real-world problem: **misinformation**.

---

## 💡 What Does It Do?

Just paste a **news headline or short snippet**, and VeriTrust will:

- Search for **real articles** on that topic using NewsAPI
- Compare your input with the top news articles using smart AI
- Give a **verdict**:
  - ✅ Likely True
  - ⚠️ Needs Verification
  - ❌ Likely False

It also shows you **which articles matched** and how close they were to your input.

---

## 🚀 Try It Out (Locally)

Here’s how you can run it on your system:

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/veritrust-fake-news-verifier.git
cd veritrust-fake-news-verifier

# 2. Install required libraries
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
