import speech_recognition as sr
import sounddevice as sd

def check_microphone():
    """Check if microphone is available"""
    try:
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        if input_devices:
            print(f"🎤 Microphones found: {len(input_devices)}")
            for i, device in enumerate(input_devices):
                print(f"  {i}: {device['name']}")
            return True
        else:
            print("❌ No microphones found")
            return False
    except:
        print("⚠️  Could not check audio devices")
        return True  # Try anyway

def listen():
    """
    Listen for voice input and convert to text
    
    Returns:
        str: Recognized text in lowercase, or empty string if failed
    """
    # Check microphone first
    if not check_microphone():
        return ""
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("🎤 Listening... (speak now)")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        # Convert audio to text
        text = recognizer.recognize_google(audio).lower()
        print(f"🗣️  You said: {text}")
        return text
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return ""
    except sr.UnknownValueError:
        print("🤔 Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"🌐 Speech recognition service error: {e}")
        return ""
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")
        print("Trying alternative method...")
        # Fallback: Try without microphone check
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            return text
        except:
            return ""