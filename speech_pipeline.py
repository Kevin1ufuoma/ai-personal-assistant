import speech_recognition as sr

def listen_to_user_voice() -> str:
    """
    Opens the physical microphone, captures your spoken words, 
    and translates them into a text string completely for free.
    """
    # Initialize the speech listening engine
    recognizer = sr.Recognizer()
    
    # Enable dynamic adjustments to ignore household room noise
    recognizer.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\n🎙️ [LISTENING] Adjusting for background room static noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("🎤 Speak your request or question out loud now...")
        try:
            # Capture speech audio waves, timing out if you remain silent for 5 seconds
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=12)
            print("🎛️ Translating audio frequencies into text lines...")
            
            # Send audio data to the free public cloud converter lane
            spoken_text = recognizer.recognize_google(audio_data)
            print(f"You said verbally: \"{spoken_text}\"")
            return spoken_text
            
        except sr.WaitTimeoutError:
            print("⚠️ Timeout: No spoken words detected.")
            return ""
        except sr.UnknownValueError:
            print("⚠️ Parsing Error: The audio signal was too faint or unclear.")
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Cloud Error: Speech translation framework briefly unavailable: {e}")
            return ""

if __name__ == "__main__":
    print("Testing Voice Capturing Pipeline Standalone...")
    captured_string = listen_to_user_voice()
    if captured_string:
        print(f"Pipeline Test Success! Captured Text: {captured_string}")
