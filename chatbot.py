import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Environment or hardcoded API keys, paste in .env
GROQ_API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("API_KEY")
GEMMA_API_KEY = os.getenv("API_KEY")
MISTRAL_API_KEY = os.getenv("API_KEY")

# Model Options
MODEL_OPTIONS = {
    "Groq (LLaMA3)": {
        "api": "groq",
        "models": ["llama3-8b-8192"]
    },
    "OpenAI (whisper-large-v3)": {
        "api": "groq",
        "models": ["whisper-large-v3"]
    },
    "Google (gemma2-9b-it)": {
        "api": "groq",
        "models": ["gemma2-9b-it"]
    },
    "Mistral (mistral-saba-24b)": {
        "api": "groq",
        "models": ["mistral-saba-24b"]
    }
}

# UI Setup
st.set_page_config("🧠 Multi-LLM Chatbot")
st.title("🧠 Multi-LLM Chatbot with Groq, OpenAI, google, Mistral")

provider = st.sidebar.selectbox("🧠 Choose LLM Provider", list(MODEL_OPTIONS.keys()))
model = st.sidebar.selectbox("🤖 Choose Model", MODEL_OPTIONS[provider]["models"])

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user prompt
if prompt := st.chat_input("Ask something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Prepare messages
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

    with st.spinner("Thinking..."):
        # Choose API handler
        api_type = MODEL_OPTIONS[provider]["api"]

        if api_type == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }

        elif api_type == "OpenAI":
            url = "distil-whisper/distil-large-v3"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }

        elif api_type == "google":
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": GEMMA_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 1000
            }

        elif api_type == "mistral":
            url = "https://console.groq.com/docs/model/mistral-saba-24b"
            headers = {
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }

        try:
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()

            if api_type == "anthropic":
                reply = data["content"][0]["text"]
            else:
                reply = data["choices"][0]["message"]["content"]

        except Exception as e:
            reply = f" Error: {e}"

        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
