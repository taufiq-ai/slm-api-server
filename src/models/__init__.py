import os
import structlog
from dotenv import load_dotenv

from llama_cpp import Llama

logger = structlog.get_logger(__name__)
load_dotenv()

LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")
CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", 1024 * 2))


def load_model(
    model_path: str = LOCAL_MODEL_PATH,
    context_window: int = CONTEXT_WINDOW,
) -> None:
    """
    load gguf formatted model from local
    """
    if not os.path.exists(model_path):
        logger.error(
            f"Recheck  .env var 'LOCAL_MODEL_PATH': '{LOCAL_MODEL_PATH}' is correct path",
            model_path=model_path,
        )
        raise FileNotFoundError(f"Model file not found at {model_path}")

    logger.info(f"Loading model", context_window=context_window, model_path=model_path)
    model = Llama(
        model_path=model_path,
        n_ctx=context_window,
    )
    return model
