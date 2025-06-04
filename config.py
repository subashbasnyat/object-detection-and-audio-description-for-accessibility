# Configuration settings
LLM_MODEL_NAME = "microsoft/phi-2"  # or "google/gemma-2b-it"
USE_OFFLINE = True  # Set to True to use offline weights with llama.cpp

TTS_VOICE = 'default'
TTS_RATE = 150

CAMERA_SOURCE = 0  # 0 for default webcam
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence to consider a detection
ENABLE_LIVE_DISPLAY = True
LOG_FILE = "logs/project.log"