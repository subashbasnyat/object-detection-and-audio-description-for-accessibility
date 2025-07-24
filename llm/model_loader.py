from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from config import LLM_MODEL_NAME


def load_model():
    print("Loading LLM...")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)

    # Load model with automatic device mapping and disk offloading support
    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL_NAME,
        torch_dtype=torch.float32,
        device_map="auto",                 # Automatically assign layers to CPU/GPU
        offload_folder="offload"          # Folder to offload weights if memory is limited
    )

    model.eval()
    print("Model loaded successfully.")
    return tokenizer, model


def query_model(tokenizer, model, img_description):
    prompt = (
        "You are an accessibility assistant. "
        "Given the following image description, write a detailed, helpful, and human-friendly explanation for a visually impaired user:\n\n"
        f"Image description: {img_description}\n\n"
        "Explanation:"
    )

    # Tokenize input and move to the model's device
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response without gradient tracking
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.8,
            top_p=0.95
        )

    # Decode and return the output text
    return tokenizer.decode(output[0], skip_special_tokens=True)
