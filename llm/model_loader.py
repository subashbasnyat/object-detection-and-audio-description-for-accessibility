from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from config import MODEL_NAME

model_name = "microsoft/phi-2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def load_model():
    print("Loading LLM...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    return tokenizer, model

def query_model(tokenizer, model, prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)