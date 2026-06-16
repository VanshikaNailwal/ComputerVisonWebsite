import os
import sys


def get_app_dir():

    # running as exe
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # development backend folder
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )


def get_storage_root():

    config_path = os.path.join(
        get_app_dir(),
        "storage_config.txt"
    )

    # installer mode
    if os.path.exists(config_path):

        with open(config_path, "r") as f:
            storage_path = f.read().strip()

            if storage_path:
                return storage_path


    # development mode
    return os.path.join(
        get_app_dir(),
        "storage"
    )



STORAGE_ROOT = get_storage_root()


EVENT_DIR = os.path.join(
    STORAGE_ROOT,
    "events"
)


EVIDENCE_DIR = os.path.join(
    STORAGE_ROOT,
    "evidence"
)


MODEL_DIR = os.path.join(
    STORAGE_ROOT,
    "models"
)



for folder in [
    EVENT_DIR,
    EVIDENCE_DIR,
    MODEL_DIR
]:
    os.makedirs(
        folder,
        exist_ok=True
    )