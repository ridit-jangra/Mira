import speech_recognition as sr
import time

r = sr.Recognizer()
mic = sr.Microphone()

try:
    while True:
        print("Listening...")
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Google API error: {e}")
        
        time.sleep(0.5)  # Brief pause
except KeyboardInterrupt:
    print("Stopped listening")
