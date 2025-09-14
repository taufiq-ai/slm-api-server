import json
from inference import infer


def get_llm_response(data: json):
    if not is_valid_input(data):
        STATUS = 400
        response = {"error": "api_key and prompt are required"}
        return STATUS, response

    payload = get_llm_payload(data)
    response = infer(**payload)
    return 200, response


def get_dummy_llm_response(data: json):
    if not is_valid_input(data):
        response = {"error": "api_key and prompt are required"}
        return 400, response

    payload = get_llm_payload(data)
    dummy_response = {
        "message": "success",
        "payload": {**payload},
    }
    return 200, dummy_response


def get_llm_payload(data: json):
    """
    Extract expected parameters from user input
    """
    return {
        # "api_key": data.get("api_key"),
        "prompt": data.get("prompt"),
        "max_tokens": data.get("max_tokens", 100),
        "temperature": data.get("temperature", 0.7),
    }


def is_valid_input(data: json):
    if not data or not data.get("api_key") or not data.get("prompt"):
        return False
    return True
