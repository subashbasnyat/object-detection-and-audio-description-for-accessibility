from PIL import Image
import os

def save_image(file, upload_folder='static/uploads'):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)
    return filepath

def process_image(image_path):
    # Add any image recognition or pre-processing here
    return f"Received image: {os.path.basename(image_path)}"
