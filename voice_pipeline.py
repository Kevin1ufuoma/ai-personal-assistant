# FIXED: Safe cloud fallback handling if pyttsx3 cannot be loaded on a headless server
try:
    import pyttsx3
    HAS_TTS = True
except ModuleNotFoundError:
    HAS_TTS = False

def speak_text(text: str):
    """
    Speaks text out loud if hardware drivers are available (Local machine).
    Gracefully logs text to console if running on a headless web server (Streamlit Cloud).
    """
    clean_text = text.replace("\n", " ").replace("*", "").replace("-", " ")
    print(f"Assistant Context Summary: {clean_text}")
    
    if HAS_TTS:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)
            engine.setProperty('volume', 1.0)
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            print(f"Local text-to-speech hardware skip: {e}")
    else:
        # Headless Cloud Mode fallback
        print("📢 Cloud execution environment detected: Skipping hardware text-to-speech audio loop.")

if __name__ == "__main__":
    speak_text("Testing your cloud-compatible voice pipeline module.")
