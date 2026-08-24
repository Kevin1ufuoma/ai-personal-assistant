import psycopg2
import streamlit as st  # <-- DEFINES 'st' IMMEDIATELY FOR THE FILE
from database_manager import DATABASE_URL
from groq import Groq

# Securely grab your key from Streamlit Cloud's secrets vault
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def get_latest_mood(user_id: int) -> str:
    """Fetches the very last mood logged by the specific authenticated cloud user."""
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT mood FROM mood_logs WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row[0] if row else "Unknown"
    except Exception:
        return "Unknown"

def generate_mood_recommendation() -> str:
    """Analyzes the user's current mood and uses Groq Cloud AI for instant recommendations."""
    if "user_id" not in st.session_state or not st.session_state.user_id:
        return "Please log into your account first."
        
    user_id = st.session_state.user_id
    user_name = st.session_state.user_name
    
    current_mood = get_latest_mood(user_id)
    
    if current_mood == "Unknown":
        return f"Hey {user_name}, I don't have a record of your cloud mood log yet. Please select a mood above to test me out!"

    prompt = (
        f"The user, {user_name}, is currently feeling '{current_mood}'. "
        f"Provide exactly one highly specific, fresh recommendation for each of these four categories to soothe or match their mood:\n"
        f"1. A Movie suggestion\n"
        f"2. A Song or music album suggestion\n"
        f"3. A quick game recommendation\n"
        f"4. A practical skill or topic they can spend 15 minutes learning right now.\n"
        f"Keep the descriptions brief, encouraging, conversational, and tailored to help with being '{current_mood}'."
    )

    client = Groq(api_key=GROQ_API_KEY)

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": f"You are a helpful AI Personal Assistant. Always address the user as {user_name}."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry {user_name}, I failed to generate cloud recommendations: {str(e)}"
