    from groq import Groq
from search_tool import search_the_web

# PASTE YOUR FRESH UNCOMPROMISED GROQ API KEY HERE INSIDE THE QUOTES
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_cloud_assistant(user_question: str, user_name: str, sex: str) -> str:
    """Sends queries to Groq's fast remote cloud infrastructure using openai/gpt-oss-120b."""
    if GROQ_API_KEY == st.secrets["GROQ_API_KEY"]:
        return f"Hey {user_name}, please add your Groq API key inside cloud_brain.py to enable my cloud mind."

    # Fetch live web data using our existing search script
    web_data = search_the_web(user_question)
    
    # Initialize the Groq Cloud Client connection node
    client = Groq(api_key=GROQ_API_KEY)
    
    system_instruction = (
        f"You are a helpful AI Personal Assistant. The user's name is {user_name}. "
        f"You must ALWAYS address the user by their name. Here is live information gathered from the web:\n"
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
        # Reverting to the exact unpacked content line your local machine relies on
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry {user_name}, my cloud network ran into an issue: {str(e)}"
