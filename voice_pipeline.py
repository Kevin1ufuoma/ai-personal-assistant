import pyttsx3

def speak_text(text: str):
    """
    Takes any text string and speaks it out loud completely 
    using the computer's internal offline voice.
    """
    # Clean out basic markdown characters that can make the engine stumble
    clean_text = text.replace("\n", " ").replace("*", "").replace("-", " ")
    
    # Initialize the speech engine
    engine = pyttsx3.init()
    
    # Adjust the speed of the voice (165 is a natural human pace)
    engine.setProperty('rate', 165)
    engine.setProperty('volume', 1.0)
    
    print(f"Assistant speaking: {clean_text}")
    
    # Queue up the text and block until it finishes speaking completely
    engine.say(clean_text)
    engine.runAndWait()

if __name__ == "__main__":
    speak_text("Hello! Your original voice pipeline is fully operational.")
