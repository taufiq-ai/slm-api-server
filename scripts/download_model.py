import os
from pathlib import Path

import structlog
from dotenv import load_dotenv

from huggingface_hub import hf_hub_download


load_dotenv()
logger = structlog.get_logger(__name__)

# Your model repo on Hugging Face
HF_REPO_ID = os.getenv("HF_REPO_ID", "taufiq-ai/qwen2.5-coder-1.5-instruct-ft")
HF_MODEL_FILE = os.getenv("HF_MODEL_FILE")
LOCAL_MODEL_DIR = os.getenv("DEFAULT_MODEL_DIR")


SAVE_DIR = Path(LOCAL_MODEL_DIR)
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def download_model(
    repo_id: str = HF_REPO_ID,
    filename: str = HF_MODEL_FILE,
    save_dir: Path = SAVE_DIR,
    repo_type: str = "model",
) -> None:
    logger.info(
        "Downloading model from Hugging Face",
        repo_id=repo_id,
        model_file=filename,
        save_dir=save_dir,
    )
    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=save_dir,
        repo_type=repo_type,
    )
    logger.info(
        "Model downloaded successfully", model_path=model_path, save_dir=save_dir
    )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Download model from Hugging Face")
    parser.add_argument(
        "--repo_id", type=str, default=HF_REPO_ID, help="Hugging Face repository ID"
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=HF_MODEL_FILE,
        help="Model file name to download",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default=LOCAL_MODEL_DIR,
        help="Directory to save the downloaded model",
    )
    args = parser.parse_args()
    download_model(
        repo_id=args.repo_id, filename=args.filename, save_dir=Path(args.save_dir)
    )


if __name__ == "__main__":
    main()
    # usage: python scripts/download_model.py --repo_id taufiq-ai/qwen2.5-coder-1.5-instruct-ft --filename qwen2.5-coder-1.5b-instruct-mt-04092025-v2.gguf --save_dir src/models/
    # or simply run `python scripts/download_model.py` to use the default values from .
