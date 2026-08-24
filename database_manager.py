import sqlite3

DB_NAME = "assistant_memory.db"
DATABASE_URL = st.secrets[""]


def initialize_database():
    """Creates the database tables for a multi-user environment from scratch."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    # 1. Multi-User Table (Includes Username and Secure Hashed Password)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sex TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 2. User-Separated Schedules Table (Includes user_id link)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            category TEXT CHECK(category IN ('health', 'business', 'personal')) NOT NULL,
            scheduled_time TEXT NOT NULL, 
            reminder_24h_sent INTEGER DEFAULT 0, 
            reminder_10h_sent INTEGER DEFAULT 0,
            reminder_1hr_sent INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 3. User-Separated Mood Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    connection.commit()
    connection.close()
    print("Multi-user database tables initialized successfully.")

def get_user():
    """Backup function to prevent older scripts from breaking."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT name, sex FROM users LIMIT 1")
    user = cursor.fetchone()
    connection.close()
    return user

if __name__ == "__main__":
    initialize_database()
