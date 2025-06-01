"""
Processes the user image and provides a description.
"""

from PIL import Image
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from ultralytics import YOLO
import cv2 

# Load BLIP model and processor once (global, so it's not reloaded every call)
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def load_image(image_path):
    """
    Loads an image from the given path.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")
    img = Image.open(image_path)
    return img

def image_to_description(image):
    """
    Uses BLIP to generate a description of the image content.
    """
    inputs = blip_processor(image, return_tensors="pt")
    with torch.no_grad():
        out = blip_model.generate(**inputs)
    description = blip_processor.decode(out[0], skip_special_tokens=True)
    return description
    

def display_image_description(image: Image.Image) -> str:
    """
    Loads an image and returns its description.
    Can be used directly in UI or logging.
    """
    description = image_to_description(image)
    print(f"[Image Description]: {description}")
    return description
