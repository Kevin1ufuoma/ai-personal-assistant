import os
import shutil
import datetime
import sqlite3
from database_manager import DB_NAME, get_user

VAULT_DIR = "alarm_vault"
ACTIVE_ALARM_PATH = os.path.join(VAULT_DIR, "active_morning_alarm.mp3")

def initialize_alarm_system():
    """Creates the local storage folder for your audio files if it doesn't exist."""
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)
        print(f"Created local audio vault directory: '{VAULT_DIR}'")

def upload_new_alarm_song(source_file_path: str) -> str:
    """
    Simulates uploading a song file into the assistant.
    Copies it to the vault, making it the active morning alarm.
    """
    initialize_alarm_system()
    
    if not os.path.exists(source_file_path):
        return f"Error: The source file '{source_file_path}' could not be found."
    
    try:
        # Overwrite the previous active alarm file safely
        shutil.copy(source_file_path, ACTIVE_ALARM_PATH)
        
        # Save the current time as the last upload date in a text configuration file
        with open(os.path.join(VAULT_DIR, "last_upload_date.txt"), "w") as f:
            f.write(datetime.date.today().strftime("%Y-%m-%d"))
            
        return "Success! Your new morning alarm song has been safely uploaded and activated."
    except Exception as e:
        return f"Failed to upload audio file: {str(e)}"

def check_if_song_change_is_due() -> bool:
    """Checks if 7 days or more have passed since your last song upload."""
    date_file = os.path.join(VAULT_DIR, "last_upload_date.txt")
    if not os.path.exists(date_file):
        return True # No upload history means a change is due immediately!
        
    with open(date_file, "r") as f:
        last_date_str = f.read().strip()
        
    last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date()
    days_passed = (datetime.date.today() - last_date).days
    
    return days_passed >= 7

def trigger_morning_alarm(authenticated_user_name: str = "User"):
    """Plays your custom uploaded song out loud to wake you up matching your user context."""
    print(f"\n⏰ [ALARM TRIGGERED] Good morning, {authenticated_user_name}! Waking you up...")
    
    if os.path.exists(ACTIVE_ALARM_PATH):
        try:
            from playsound import playsound
            print(f"Playing your custom alarm track out loud completely offline...")
            playsound(ACTIVE_ALARM_PATH)
        except Exception as e:
            print(f"Audio file playback execution error: {e}")
    else:
        print("⚠️ No custom alarm song uploaded this week! Using standard buzzer alert.")


if __name__ == "__main__":
    print("Testing Alarm System Initialization...")
    initialize_alarm_system()
    print("Is a song update required this week?", check_if_song_change_is_due())
