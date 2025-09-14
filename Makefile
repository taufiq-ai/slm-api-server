run:
	uv run python src/server.py

download-model:
	uv run python -m scripts.download_model