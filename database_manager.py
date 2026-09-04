import psycopg2
import streamlit as st  

DB_NAME = "assistant_memory.db"

# FIXED: Standardizes secret fetching safely with a working, global IPv4 pooler fallback URL
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = "postgresql://postgres.qzqnwfzkzgiupopaycoz:0PYdI4UHZlRzMyHlTxTTCefuwLDMc6A5@://supabase.com"

def initialize_cloud_database():
    """Establishes tables directly on the cloud serverless database."""
    # Ensure a blank configuration doesn't crash into local Unix sockets
    db_to_use = DATABASE_URL if DATABASE_URL else "postgresql://postgres.qzqnwfzkzgiupopaycoz:0PYdI4UHZlRzMyHlTxTTCefuwLDMc6A5@://supabase.com"
    
    connection = psycopg2.connect(db_to_use)
    cursor = connection.cursor()
    
    # 1. Cloud Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            sex TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 2. Cloud User-Separated Schedules Table
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
    
    # 3. Cloud User-Separated Mood Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            mood TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    ''')
    
    # 4. Cloud Contacts Table Natively
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            contact_name TEXT NOT NULL,
            call_time TIMESTAMP
        )
    ''')
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Cloud database tables initialized successfully!")

def initialize_database():
    """Backup initialization execution call."""
    initialize_cloud_database()

if __name__ == "__main__":
    initialize_cloud_database()
