import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests
import base64

# Load TinyLlama model and tokenizer only once
# Load GPT-2 model and tokenizer only once
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    return tokenizer, model

tokenizer, model = load_model()


# Function to generate response from local model with proper instruction formatting
def generate_jarvis_response(prompt):
    try:
        chat_prompt = f"""You are Jarvis, an intelligent assistant created by Rehan Hussain.
Your job is to answer clearly, respectfully, and helpfully.

Human: {prompt}
Jarvis:"""

        inputs = tokenizer.encode(chat_prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=200,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Jarvis:")[-1].strip()
    except Exception as e:
        return f"Jarvis encountered an error: {e}"

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
        Jarvis is your futuristic AI assistant, now running locally using TinyLlama.
        No external API needed for chat!
    """)
