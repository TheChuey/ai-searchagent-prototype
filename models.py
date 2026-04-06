import requests
import json # Added for stream parsing
from prompts import SYSTEM_PROMPT

# AI STRUCTURE NOTE: 
# Using 'yield' turns these functions into Generators for Streamlit's write_stream.

def get_models():
    try:
        res = requests.get("http://localhost:11434/api/tags")
        data = res.json()
        return [m["name"] for m in data.get("models", [])]
    except:
        return []

def call_local_model(messages, model):
    # Combine ALL messages into one prompt (this preserves memory)
    prompt = "\n\n".join([
        f"{m['role'].upper()}: {m['content']}"
        for m in messages
    ])
    payload = {"model": model, "prompt": prompt, "stream": True} # Enabled Streaming

    # We use stream=True in the request to get chunks of data
    res = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)
    
    for line in res.iter_lines():
        if line:
            chunk = json.loads(line.decode('utf-8'))
            token = chunk.get("response", "")
            yield token # BEGINNER TIP: 'yield' sends the word to the UI immediately

def call_api_model(messages, model):
    # Placeholder generator
    full_text = f"[API MODE ACTIVE] Model: {model}. Streaming simulation started..."
    for word in full_text.split():
        yield word + " "

def route_request(messages, model, backend):
    # 1. Create the 'Rules' message
    system_message = {"role": "system", "content": SYSTEM_PROMPT}

    # 2. Build the full context stack
    # [Rules] + [Past Chat/Research] + [Current Question]
    full_context = [system_message] + messages

    # 3. Call the model
    # By sending the list this way, the AI is "Grounding" itself 
    # in your history before answering.
    response = ollama.chat(
        model=model,
        messages=full_context,
        stream=True
    )
    for chunk in response:
        yield chunk['message']['content']