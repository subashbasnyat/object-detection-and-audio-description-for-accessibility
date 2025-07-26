import os
import uuid
import time
import glob
from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from tts.tts_engine import speak_text, speak_text_live  

# App Setup
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
USE_WHITE_BALANCE = True
CLEANUP_AGE = 3600  # seconds

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Model Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Utility Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def correct_white_balance(frame):
    result = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)

    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])

    result[:, :, 1] -= ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] -= ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)

    result = np.clip(result, 0, 255).astype(np.uint8)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

def generate_description(image):
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

def cleanup_upload_folder(folder, max_age):
    now = time.time()
    for f in glob.glob(os.path.join(folder, '*')):
        if os.path.isfile(f) and os.stat(f).st_mtime < now - max_age:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Failed to remove {f}: {e}")

# ----------- CAMERA FEED ROUTE -----------
def generate_frames():
    camera = cv2.VideoCapture(0)
    frame_count = 0
    FRAME_SKIP = 15  # Adjust for performance
    SPEAK_INTERVAL = 5  # seconds

    last_caption = ""
    last_spoken_time = time.time()

    while True:
        success, frame = camera.read()
        if not success:
            break

        if USE_WHITE_BALANCE:
            frame = correct_white_balance(frame)

        frame_count += 1
        if frame_count % FRAME_SKIP != 0:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        description = generate_description(pil_image)

        current_time = time.time()
        should_speak = False

        if description:
            if description != last_caption:
                should_speak = True
                last_caption = description
                last_spoken_time = current_time
            elif current_time - last_spoken_time >= SPEAK_INTERVAL:
                should_speak = True
                last_spoken_time = current_time

            if should_speak:
                print("[Live Camera Caption]:", description)
                speak_text_live(description)

        # Draw caption
        y_offset = 30
        for line in description.split(', '):
            cv2.putText(frame, line, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            y_offset += 30

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()

# ----------- ROUTES -----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/camera')
def camera_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['POST'])
def upload_image():
    response_text = ""
    audio_file = ""

    cleanup_upload_folder(app.config['UPLOAD_FOLDER'], CLEANUP_AGE)

    if 'image' not in request.files:
        return render_template('index.html', response="No image part", audio_file=audio_file)

    image = request.files['image']
    if image.filename == '':
        return render_template('index.html', response="No selected file", audio_file=audio_file)

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(file_path)

        pil_image = Image.open(file_path).convert('RGB')
        response_text = generate_description(pil_image)

        audio_filename = f"{uuid.uuid4().hex}.mp3"
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        speak_text(response_text, audio_file_path)

        audio_file = f"uploads/{audio_filename}"
        return render_template('index.html', response=response_text, audio_file=audio_file)

    return render_template('index.html', response="Invalid file type", audio_file=audio_file)

# ----------- MAIN -----------
if __name__ == '__main__':
    app.run(debug=True)
