"""
Offline Text-to-Speech using pyttsx3
"""
import pyttsx3
from config import TTS_RATE, TTS_VOICE

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', TTS_RATE)
    voices = engine.getProperty('voices')

    # Optional: Choose specific voice
    if TTS_VOICE != 'default':
        for voice in voices:
            if TTS_VOICE.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.say(text)
    engine.runAndWait()
