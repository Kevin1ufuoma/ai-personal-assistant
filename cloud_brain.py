import streamlit as st  
from groq import Groq

# Safely import search tool
try:
    from search_tool import search_the_web
except ModuleNotFoundError:
    def search_the_web(query):
        return "Search tool module loading..."

# Securely grab your key from Streamlit Cloud's secrets vault
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_cloud_assistant(user_question: str, user_name: str, sex: str) -> str:
    """Sends queries to Groq's fast remote cloud infrastructure using openai/gpt-oss-120b."""
    web_data = search_the_web(user_question)
    client = Groq(api_key=GROQ_API_KEY)
    
    system_instruction = (
        f"You are a helpful AI Personal Assistant. The user's name is {user_name}.\n"
        f"Here is live information gathered from the web to help answer the user's question:\n"
        f"=== WEB DATA ===\n{web_data}\n===============\n"
        f"Synthesize this into a crisp, conversational voice-optimized reply."
    )
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_question}
            ]
        )
        return completion.choices.message.content
    except Exception as e:
        return f"Sorry {user_name}, my cloud network ran into an issue: {str(e)}"
