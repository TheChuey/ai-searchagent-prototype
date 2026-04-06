from models import call_local_model, call_api_model
from prompts import SYSTEM_PROMPT

def route_request(messages, model, backend):

    # Inject system rules at the top
    system_message = {"role": "system", "content": SYSTEM_PROMPT}

    # FULL CONTEXT (this is the key fix)
    full_context = [system_message] + messages

    if backend == "Local":
        return call_local_model(full_context, model)

    elif backend == "API":
        return call_api_model(full_context, model)

    return "Invalid backend selected"