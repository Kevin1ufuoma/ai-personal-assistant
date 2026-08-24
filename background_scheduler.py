import psycopg2
import datetime
from voice_pipeline import speak_text
from database_manager import DATABASE_URL

def check_and_send_reminders():
    """Scans the Render Cloud Database for upcoming schedules across ALL user profiles."""
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        now = datetime.datetime.now()
        
        cursor.execute('''
            SELECT s.id, s.title, s.category, s.scheduled_time, s.reminder_24h_sent, 
                   s.reminder_10h_sent, s.reminder_1hr_sent, u.name 
            FROM schedules s
            JOIN users u ON s.user_id = u.id
        ''')
        schedules = cursor.fetchall()
        
        for row in schedules:
            db_id, title, category, sched_time, r24, r10, r1, user_name = row
            time_difference = sched_time - now
            hours_remaining = time_difference.total_seconds() / 3600.0
            
            if 23.9 <= hours_remaining <= 24.1 and not r24:
                speak_text(f"Hello {user_name}, this is your 24 hour warning for your cloud {category} activity: {title}.")
                cursor.execute("UPDATE schedules SET reminder_24h_sent = 1 WHERE id = %s", (db_id,))
            elif 9.9 <= hours_remaining <= 10.1 and not r10:
                speak_text(f"Excuse me {user_name}, you have a private {category} calendar event in 10 hours: {title}.")
                cursor.execute("UPDATE schedules SET reminder_10h_sent = 1 WHERE id = %s", (db_id,))
            elif 0.9 <= hours_remaining <= 1.1 and not r1:
                speak_text(f"Attention {user_name}! Your important {category} activity, {title}, begins in exactly one hour.")
                cursor.execute("UPDATE schedules SET reminder_1hr_sent = 1 WHERE id = %s", (db_id,))
                
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Background Tracker Network Delay: {e}")

def trigger_scheduled_contact_voice_calls():
    """
    Scans the database and fires a real-time voice reminder 
    the exact minute a scheduled phone call is due.
    """
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        now = datetime.datetime.now()
        
        # Pull entries where the scheduled call time matches the current window
        cursor.execute('''
            SELECT c.id, u.name, c.contact_name, c.call_time 
            FROM contacts c
            JOIN users u ON c.user_id = u.id
        ''')
        records = cursor.fetchall()
        
        for row in records:
            db_id, owner_name, target_friend, call_time = row
            if call_time:
                # Calculate time difference
                time_delta = call_time - now
                minutes_remaining = time_delta.total_seconds() / 60.0
                
                # If the call is due within the current minute window, speak out loud!
                if -1.0 <= minutes_remaining <= 1.0:
                    speak_text(f"Attention {owner_name}, this is your scheduled reminder. It is time to make your phone call to {target_friend}.")
                    
                    # Optional: Wipe or mark the call time as handled so it doesn't loop repeat
                    cursor.execute("UPDATE contacts SET call_time = NULL WHERE id = %s", (db_id,))
                    
        connection.commit()
        cursor.close()
        connection.close()
            
    except Exception as e:
        print(f"Contact Voice Tracker Error: {e}")
