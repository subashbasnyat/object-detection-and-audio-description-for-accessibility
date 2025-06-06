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
    Selects prompt templates based on keywords in the image description.
    """
    lower_desc = image_description.lower()
    context_templates = []

    if any(word in lower_desc for word in ["person", "people", "man", "woman", "child"]):
        context_templates += [
            "Describe the people and their actions in the image for a visually impaired user.",
            "Explain what the people are doing and how they interact with the environment.",
            "Summarize the appearance and activities of the individuals in the picture."
        ]
    if any(word in lower_desc for word in ["animal", "dog", "cat", "bird"]):
        context_templates += [
            "Describe the animals present and their behavior in the image.",
            "Explain how the animals are interacting with their surroundings or people."
        ]
    if any(word in lower_desc for word in ["object", "car", "tree", "building", "food"]):
        context_templates += [
            "List and describe the main objects visible in the image.",
            "Explain the arrangement and significance of the objects in the scene."
        ]
    if not context_templates:
        context_templates = PROMPT_TEMPLATES  # fallback to generic templates

    selected_template = random.choice(context_templates)
    return f"{selected_template}\n\nImage Description: {image_description}"
