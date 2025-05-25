from flask import Flask, render_template, request
from utils.image_processor import save_image, process_image
from utils.audio_handler import text_to_speech
from utils.llm_handler import query_llm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        image = request.files['image']
        if image:
            path = save_image(image)
            img_description = process_image(path)
            llm_output = query_llm(f"Describe this: {img_description}")
            audio_path = text_to_speech(llm_output, 'static/response.mp3')
            response = llm_output
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
