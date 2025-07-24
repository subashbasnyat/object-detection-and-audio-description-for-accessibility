import numpy as np
import cv2
from PIL import Image
from tts.color_correction import correct_white_balance

def preprocess_pil_image(pil_img: Image.Image) -> Image.Image:
    """
    Convert PIL image to OpenCV, apply white balance correction,
    then convert back to PIL image.
    """
    # PIL (RGB) -> OpenCV (BGR)
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    # Apply white balance correction
    corrected_cv_img = correct_white_balance(cv_img)
    
    # OpenCV (BGR) -> PIL (RGB)
    corrected_pil_img = Image.fromarray(cv2.cvtColor(corrected_cv_img, cv2.COLOR_BGR2RGB))
    
    return corrected_pil_img
