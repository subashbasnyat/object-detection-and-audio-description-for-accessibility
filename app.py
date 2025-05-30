# from flask import Flask, render_template, request
# from image_processing.image_processor import save_image, process_image
# from utils.audio_handler import text_to_speech
# from llm.model_loader import query_model, load_model
# from tts.tts_engine import speak_text

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     response = None
#     if request.method == 'POST':
#         image = request.files['image']
#         if image:
#             path = save_image(image)
#             img_description = process_image(path)
#             llm_output = query_model(f"Describe this: {img_description}")
#             audio_path = text_to_speech(llm_output, 'static/response.mp3')
#             response = llm_output
#     return render_template('index.html', response=response)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template
from llm.model_loader import load_model, query_model
from tts.tts_engine import speak_text
from image_processing.image_processor import load_image, image_to_description, display_image_description
from prompts.prompt_templates import generate_prompt
import os
from PIL import Image
import time

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

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
