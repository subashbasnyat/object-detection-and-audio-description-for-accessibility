import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os

def text_to_speech(text, filename='response.mp3'):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
