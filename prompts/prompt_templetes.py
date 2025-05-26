"""
Prompt templates for LLM
"""
import random

PROMPT_TEMPLATES = [
    "Describe the image in a way that helps a visually impaired person understand it.",
    "Summarize the main elements in the image clearly and concisely for a blind user.",
    "What is happening in the image? Describe it as if explaining to someone who can’t see.",
    "Give an accessible verbal summary of this image for someone who is visually impaired.",
    "Please describe the key objects, people, or actions in this picture.",
    "Imagine you’re guiding a person through this image without showing it. What would you say?",
    "Tell me what’s in the image using simple and clear language suitable for an audio assistant.",
    "What important features or objects are visible in the image that should be mentioned?",
    "Explain the scene like you're reading it aloud for someone who cannot see it.",
    "Give a clear spoken explanation of what this image represents.",
    "How would you describe this image over a phone call to a blind friend?",
    "Identify the key items in this image and explain their arrangement.",
    "What do you think is the focus of this image? Describe it out loud.",
    "Convert the image into a helpful verbal description for a disabled user.",
    "Describe the environment, people, or actions shown in the image in simple terms.",
    "Break down the visual content into a short spoken paragraph for accessibility.",
    "Help a disabled user imagine what’s in this image using words.",
    "Describe the image in a slow, detailed, and supportive way for audio playback.",
    "Create an audio guide from the visual elements you see in this image.",
    "Translate this picture into a descriptive sentence that can be spoken aloud.",
]

def generate_prompt(image_description: str):
    """
    Combines image description and a randomly selected accessible prompt template.
    """
    selected_template = random.choice(PROMPT_TEMPLATES)
    return f"{selected_template}\n\nImage Description: {image_description}"
