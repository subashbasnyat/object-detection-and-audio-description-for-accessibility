from llm.model_loader import load_model, query_model

def test_query():
    tokenizer, model = load_model()
    result = query_model(tokenizer, model, "Which light is glowing now?")
    assert isinstance(result, str) and len(result) > 0
