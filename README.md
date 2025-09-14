# slm-api-server

A lightweight **Python API server** for running inference on local or self-hosted LLMs.

* Loads GGUF-formatted models from the `src/models/` directory (via [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/latest/)).
* Exposes a simple `/inference/` endpoint for text generation.

## Features

* ✅ REST API with `POST /inference/` and `GET /healthz/`
* ✅ Supports prompts as plain strings or role-based message lists
* ✅ Easily extensible for new models and endpoints


## Setup

```bash
git clone https://github.com/taufiq-ai/slm-api-server.git
cd slm-api-server
cp .env.example .env
uv sync
make download-model # downloads my ft-model from hf repo
make run
```

## Usage

### Health Check

```bash
curl http://0.0.0.0:8000/healthz/
# ok
```

### Inference

```bash
curl -X POST http://0.0.0.0:8000/inference/ \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sk-123456",
    "prompt": "What is list comprehension?",
    "max_tokens": 150,
    "temperature": 0.8
  }'
```

**Request Parameters**

```py
api_key: str               # required (but not strictly checked, send a random value)
prompt: str | List[dict]   # required
max_tokens: int            # optional, default=100
temperature: float         # optional, default=0.7
```

**Sample Response**

```json
{
  "id": "chatcmpl-d3003005-7a6b-4081-9e1c-8ae75d2ba642",
  "object": "chat.completion",
  "created": 1757872921,
  "model": "src/models/qwen2.5-coder-1.5b-instruct-mt-04092025-v2.gguf",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "List comprehension is a concise way to create lists in Python..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 32,
    "total_tokens": 64
  }
}
```

## Contributing

Contributions are welcome!

* Fork the repo & create a feature branch.  
* Submit a PR with clear description and test coverage.  
