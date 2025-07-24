import pyttsx3
from config import TTS_RATE, TTS_VOICE

engine = pyttsx3.init()
engine.setProperty('rate', TTS_RATE)
engine.setProperty('voice', TTS_VOICE)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
