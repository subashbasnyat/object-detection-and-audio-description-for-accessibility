from flask import Flask, request, render_template, Response
from llm.model_loader import load_model, query_model
from tts.tts_engine import speak_text, speak_text_live
from image_processing.image_processor import load_image, image_to_description, display_image_description
from prompts.prompt_templates import generate_prompt
from tts.color_correction import correct_white_balance
import os
from PIL import Image
import time
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model once when app starts
tokenizer, model = load_model()

@app.route('/', methods=['GET', 'POST'])
def upload():
    response_text = ""
    audio_file = None

    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            img = load_image(image_path)
            img_description = display_image_description(img)
            response_text = img_description

            # Generate a unique filename for each audio
            audio_filename = f'response_{int(time.time())}.mp3'
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            speak_text(response_text, audio_path)
            audio_file = f'uploads/{audio_filename}'

    return render_template('index.html', response=response_text, audio_file=audio_file)

    # return render_template('index.html', response=response_text)

# ----------- CAMERA FEED ROUTE -----------
def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 for default USB webcam

    last_spoken_time = 0  # track last spoken time
    speak_interval = 3    # seconds between speech outputs

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Step 1: Apply white balance correction (optional)
        frame_corrected = correct_white_balance(frame)

        # Step 2: Convert BGR OpenCV image to RGB PIL image
        pil_img = Image.fromarray(cv2.cvtColor(frame_corrected, cv2.COLOR_BGR2RGB))

        # Step 3: Get description from BLIP (expects PIL image)
        description = display_image_description(pil_img)

        # Speak out loud every X seconds only
        current_time = time.time()
        if current_time - last_spoken_time > speak_interval:
            speak_text_live(description)
            last_spoken_time = current_time

        # Optional: display detected object labels on frame
        for i, obj in enumerate(description.split(', ')):
            cv2.putText(frame, obj, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/camera')
def camera():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
