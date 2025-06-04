from flask import Flask, request, render_template, Response
from llm.model_loader import load_model, query_model
from tts.tts_engine import speak_text
from image_processing.image_processor import load_image, image_to_description, display_image_description
from prompts.prompt_templates import generate_prompt
import os
from PIL import Image
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model once when app starts
tokenizer, model = load_model()

@app.route('/', methods=['GET', 'POST'])
def upload():
    response_text = ""
    image_path = None

    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            img = load_image(image_path)
            img_description = display_image_description(img)
            response_text = img_description

            # Generate audio from the description and save it
            audio_filename = 'response.mp3'
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            speak_text(response_text, audio_path)  # This should save the full response as audio
            audio_file = f'uploads/{audio_filename}'
            return render_template('index.html', response=response_text, audio_file=audio_file)

    return render_template('index.html', response=response_text)

# ----------- CAMERA FEED ROUTE -----------
def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 for default USB webcam

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Example: run object detection on each frame (use your detection logic here)
        detected_objects = display_image_description(frame)

        # Optional: display detected object labels on frame
        for i, obj in enumerate(detected_objects.split(', ')):
            cv2.putText(frame, obj, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame in streaming format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/camera')
def camera():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
