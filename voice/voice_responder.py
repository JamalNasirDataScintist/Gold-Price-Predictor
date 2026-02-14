import pyttsx3

# Initialize engine once
_engine = None

def get_engine():
    """Get or initialize the TTS engine"""
    global _engine
    if _engine is None:
        try:
            _engine = pyttsx3.init()
            # Configure voice settings
            _engine.setProperty("rate", 170)  # Speech speed
            _engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)
            
            # Get available voices
            voices = _engine.getProperty('voices')
            if voices:
                # Use first available voice
                _engine.setProperty('voice', voices[0].id)
                
        except Exception as e:
            print(f"❌ Failed to initialize TTS engine: {e}")
            return None
    return _engine

def speak(text):
    """
    Convert text to speech
    
    Args:
        text (str): Text to speak
    """
    try:
        engine = get_engine()
        if engine:
            print(f"🔊 Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
        else:
            print(f"📢 (Text only): {text}")
            
    except Exception as e:
        print(f"❌ Speech synthesis error: {e}")
        print(f"📝 (Failed to speak): {text}")