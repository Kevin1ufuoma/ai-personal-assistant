import streamlit as st
import datetime
import psycopg2
import hashlib
import os
from database_manager import DATABASE_URL  # Import your live cloud link string
from cloud_brain import ask_cloud_assistant
from mood_recommendation import generate_mood_recommendation
from voice_pipeline import speak_text

# Set up page configurations
st.set_page_config(page_title="AI Personal Assistant Cloud", page_icon="🤖", layout="centered")

# Securely hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize cloud session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_sex" not in st.session_state:
    st.session_state.user_sex = ""

# --- FORCE CLOUD TABLE INITIALIZATION ON WEB STARTUP ---
def force_table_creation():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Force User Table Creation Natively
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                sex TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        
        # 2. Force Schedules Table Creation Natively
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL, 
                reminder_24h_sent INTEGER DEFAULT 0, 
                reminder_10h_sent INTEGER DEFAULT 0,
                reminder_1hr_sent INTEGER DEFAULT 0
            )
        ''')
        
        # 3. Force Mood Logs Table Creation Natively
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_logs (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                mood TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        ''')
        
        # 4. Force Contacts Table Creation Natively
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                contact_name TEXT NOT NULL,
                call_time TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Render Cloud Database Structural Tables Synced Successfully!")
    except Exception as e:
        st.error(f"Critical Database Sync Error: {e}")

# We force execution right here!
force_table_creation()


# --- AUTHENTICATION INTERFACE (CLOUD GATEWAY LAYER) ---
if not st.session_state.logged_in:
    st.title("🤖 Welcome to AI Assistant Cloud")
    auth_mode = st.radio("Choose Action:", ["Login to Your Account", "Create New Account"])
    
    if auth_mode == "Create New Account":
        st.subheader("📝 Sign Up New User")
        new_name = st.text_input("Full Name:")
        new_username = st.text_input("Choose Unique Username:")
        new_password = st.text_input("Create Password:", type="password")
        new_sex = st.selectbox("Your Sex:", ["Male", "Female"])
        
        if st.button("Register & Create Workspace"):
            if new_name and new_username and new_password:
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                try:
                    h_pass = hash_password(new_password)
                    cursor.execute(
                        "INSERT INTO users (name, sex, username, password_hash) VALUES (%s, %s, %s, %s)",
                        (new_name, new_sex, new_username, h_pass)
                    )
                    conn.commit()
                    st.success("Account created successfully in Cloud DB! Please switch to Login mode above.")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                st.warning("Please fill out all available fields.")
                
    elif auth_mode == "Login to Your Account":
        st.subheader("🔑 Secure Log In")
        login_username = st.text_input("Username:")
        login_password = st.text_input("Password:", type="password")
        
        if st.button("Log In"):
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            h_pass = hash_password(login_password)
            
            cursor.execute(
                "SELECT id, name, sex FROM users WHERE username = %s AND password_hash = %s",
                (login_username, h_pass)
            )
            user_found = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_found:
                st.session_state.logged_in = True
                st.session_state.user_id = user_found[0]
                st.session_state.user_name = user_found[1]
                st.session_state.user_sex = user_found[2]
                
                # Original stable voice greeting
                speak_text(f"Access granted. Welcome back to your cloud workspace, {st.session_state.user_name}.")
                st.rerun()
            else:
                st.error("Invalid username or password configuration. Try again.")

# --- CORE APP WORKSPACE (AUTHENTICATED ONLY) ---
else:
    st.sidebar.title(f"👤 Account: {st.session_state.user_name}")
    st.sidebar.write(f"Cloud User Token: #{st.session_state.user_id}")
    if st.sidebar.button("Secure Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.session_state.user_sex = ""
        st.rerun()

    st.title("🤖 My AI Personal Assistant Cloud Panel")
    
    # --- SECTION 1: HIGH-SPEED CLOUD BRAIN (RESTORED ORIGINAL) ---
    st.markdown("---")
    st.header("🔍 Ask Cloud Assistant")
    
    from speech_pipeline import listen_to_user_voice
    if "speech_input_text" not in st.session_state:
        st.session_state.speech_input_text = ""

    if st.button("🎙️ Tap to Speak Your Question"):
        st.info("Listening... Look at your command terminal window and speak clearly into your mic!")
        spoken_result = listen_to_user_voice()
        if spoken_result:
            st.session_state.speech_input_text = spoken_result
            st.success(f"Captured Speech: \"{spoken_result}\"")
        else:
            st.warning("I couldn't catch that. Please click the button and try speaking again.")

    user_query = st.text_input("Type your question here (Groq API Engine):", value=st.session_state.speech_input_text, key="restored_main_query_bar")

    if st.button("Submit Question"):
        if user_query:
            with st.spinner("High-speed Cloud AI processing request..."):
                ai_reply = ask_cloud_assistant(user_query, st.session_state.user_name, st.session_state.user_sex)
                st.success("Cloud Response Generated!")
                st.write(ai_reply)
                
                st.session_state.speech_input_text = ""
                speak_text(ai_reply)

    # --- SECTION 2: CATEGORIZED SCHEDULES MANAGEMENT ---
    st.markdown("---")
    st.header("📅 Cloud Schedule Management")

    task_title = st.text_input("Task / Event Title:")
    task_category = st.selectbox("Category:", ["Health", "Business", "Personal"])
    task_date = st.date_input("Event Date:", datetime.date.today())
    task_time = st.time_input("Event Time:", datetime.time(9, 0))

    if st.button("Save Schedule"):
        if task_title:
            combined_dt = datetime.datetime.combine(task_date, task_time)
            
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO schedules (title, category, scheduled_time, user_id) VALUES (%s, %s, %s, %s)",
                (task_title, task_category.lower(), combined_dt, st.session_state.user_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
            
            st.balloons()
            st.success(f"Successfully saved '{task_title}' to your secure cloud timeline!")

    # --- SECTION 3: CLOUD MOOD CHECK-IN ---
    st.markdown("---")
    st.header("🎭 Daily Mood Check-in")
    selected_mood = st.selectbox("How is your mood right now?", ["Happy", "Bored", "Sad", "Stressed", "Tired"])

    if st.button("Log Mood & Get Recommendations"):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "INSERT INTO mood_logs (mood, timestamp, user_id) VALUES (%s, %s, %s)", 
                (selected_mood, timestamp, st.session_state.user_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
            
            st.info(f"Mood '{selected_mood}' successfully saved to your cloud profile.")
            
            with st.spinner("AI is calculating custom lifestyle suggestions..."):
                recommendations = generate_mood_recommendation()
                st.subheader("🤖 Your Personalized Recommendations")
                st.write(recommendations)
                speak_text(recommendations)
                
        except Exception as e:
            st.error(f"Mood Check-in Failed: {str(e)}")

    # --- SECTION 4: UPGRADED CALL REMINDER MANAGEMENT ---
    st.markdown("---")
    st.header("📞 Scheduled Call Contact Saver")
    new_contact = st.text_input("Enter Contact Name to Save:")
    
    call_date = st.date_input("Schedule Call Date:", datetime.date.today(), key="call_date_picker")
    call_time = st.time_input("Schedule Call Time:", datetime.time(12, 0), key="call_time_picker")
    
    if st.button("Save Contact & Schedule Call"):
        if new_contact:
            local_dt = datetime.datetime.combine(call_date, call_time)
            combined_call_dt = local_dt - datetime.timedelta(hours=1)  # West Africa timezone correction
            
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (user_id, contact_name, call_time) VALUES (%s, %s, %s)", 
                (st.session_state.user_id, new_contact, combined_call_dt)
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"Successfully scheduled a call with '{new_contact}'!")
            st.rerun()
            
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT contact_name, call_time FROM contacts WHERE user_id = %s AND call_time IS NOT NULL ORDER BY call_time ASC", (st.session_state.user_id,))
    all_contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if all_contacts:
        st.write("**Your Scheduled Voice Reminder Calls:**")
        for c in all_contacts:
            name_str = c[0]
            local_display_time = c[1] + datetime.timedelta(hours=1)
            time_str = local_display_time.strftime('%Y-%m-%d %H:%M')
            st.write(f"- **{name_str}** scheduled for: {time_str}")

    # --- SECTION 5: MORNING ALARM WORKSPACE ---
    st.markdown("---")
    st.header("⏰ Custom Weekly Morning Alarm File Upload")
    VAULT_DIR = "alarm_vault"
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)
        
    uploaded_audio = st.file_uploader("Choose an MP3 song to wake you up each morning:", type=["mp3"])
    if uploaded_audio is not None:
        if st.button("Activate Selected Track"):
            active_alarm_path = os.path.join(VAULT_DIR, "active_morning_alarm.mp3")
            with open(active_alarm_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())
            with open(os.path.join(VAULT_DIR, "last_upload_date.txt"), "w") as f:
                f.write(datetime.date.today().strftime("%Y-%m-%d"))
            st.success("Success! Your morning alarm song has been safely activated in the background vault.")
