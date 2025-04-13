import streamlit as st
import torch
import requests
import base64
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return tokenizer, model

tokenizer, model = load_model()

def generate_jarvis_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=128,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.1
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response.split("Answer:")[-1].strip()

# News API (still requires key)
news_api_key = "MzVkNjIzMGUwMWY5NDI0ZGIwYjdlOWNmZTg1YTUzOWQ="  # Base64 encoded
news_api_key = base64.b64decode(news_api_key).decode("utf-8")

def fetch_news():
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={news_api_key}'
    try:
        news_response = requests.get(news_url, verify=False)
        news_data = news_response.json()
        if news_data['status'] == 'ok':
            return [(article['title'], article['description'], article['url']) for article in news_data['articles'][:5]]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Styling (placeholder)
st.markdown("...", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.subheader("Navigation")
    menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
    choice = st.radio("Select a feature:", menu, key="navigation_menu")
    st.subheader("Chat History")
    if st.session_state.chat_history:
        for idx, message in enumerate(st.session_state.chat_history):
            st.write(f"{idx + 1}. {message}")
    else:
        st.write("No chat history yet.")
    st.markdown("---")
    st.subheader("Developer Info")
    st.write("Created by **Rehan Hussain**.")
    st.write("Contact: rehan9644coc@gmail.com")

# Main App Logic
st.title("JARVIS")

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    user_input = st.text_input("Type your question below:")
    if st.button("Submit"):
        if user_input:
            st.session_state.chat_history.append(user_input)
            response = generate_jarvis_response(user_input)
            st.success(f"**Jarvis:** {response}")

elif choice == "Tech News":
    st.header("Latest Tech News")
    news = fetch_news()
    if news:
        for title, description, url in news:
            st.markdown(f"### [{title}]({url})")
            st.write(description)
            st.markdown("---")
    else:
        st.error("Unable to fetch news at this time.")

elif choice == "About Jarvis":
    st.header("About Jarvis")
    st.write("Created by **Rehan Hussain** without external AI APIs.")
    st.write("""
        Jarvis is your futuristic AI assistant, now running locally using Phi-2.
        No external API needed for chat!
    """)
