# --- FORCE CLOUD TABLE INITIALIZATION ON WEB STARTUP ---
def force_table_creation():
    try:
        # Import the runtime connection lookup helper dynamically
        from database_manager import get_database_url
        db_string = get_database_url()
        
        conn = psycopg2.connect(db_string)
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
        print(f"Critical Database Sync Error: {e}")

# We force execution right here!
force_table_creation()
