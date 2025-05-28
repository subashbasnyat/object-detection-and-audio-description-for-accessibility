from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from config import LLM_MODEL_NAME


def load_model():
    print("Loading LLM...")
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, torch_dtype=torch.float32,
    device_map="auto"  # will use GPU if available, otherwise CPU
    )
    model.eval()
    print("Model loaded successfully.")
    return tokenizer, model

def query_model(tokenizer, model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)