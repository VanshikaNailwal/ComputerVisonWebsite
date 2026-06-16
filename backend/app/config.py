import os

from pathlib import Path

from pydantic_settings import BaseSettings





# ----------------------------------
# Base Directory
# ----------------------------------

BASE_DIR = (

    Path(__file__)

    .resolve()

    .parents[2]

)








# ----------------------------------
# Storage Resolver
#
# Priority:
# 1. Installer selected path
#    backend/storage_config.txt
#
# 2. Development fallback
#    backend/storage
# ----------------------------------

def get_storage_dir():


    config_file = (

        BASE_DIR

        /

        "storage_config.txt"

    )



    if config_file.exists():


        storage_path = (

            config_file

            .read_text()

            .strip()

        )



        if storage_path:


            return Path(

                storage_path

            )






    return (

        BASE_DIR

        /

        "storage"

    )









# ----------------------------------
# Storage Paths
# ----------------------------------

STORAGE_DIR = get_storage_dir()


print("🔥 STORAGE USED:", STORAGE_DIR)
print("🔥 MODEL PATH:", MODEL_DIR)
print("🔥 EVIDENCE PATH:", EVIDENCE_DIR)
print("🔥 EVENT PATH:", EVENT_DIR)

MODEL_DIR = (

    STORAGE_DIR

    /

    "models"

)


EVIDENCE_DIR = (

    STORAGE_DIR

    /

    "evidence"

)


EVENT_DIR = (

    STORAGE_DIR

    /

    "events"

)







# create folders automatically

for folder in [

    STORAGE_DIR,

    MODEL_DIR,

    EVIDENCE_DIR,

    EVENT_DIR

]:


    folder.mkdir(

        parents=True,

        exist_ok=True

    )










# ----------------------------------
# Settings
# ----------------------------------

class Settings(BaseSettings):

    """
    Application configuration class.

    Loads:
    - database settings from .env
    - storage path from installer config
    """



    # DATABASE

    DATABASE_URL: str





    # SECURITY

    SECRET_KEY: str


    ALGORITHM: str = "HS256"


    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60







    # STORAGE

    STORAGE_PATH: str = str(

        STORAGE_DIR

    )


    MODEL_PATH: str = str(

        MODEL_DIR

    )


    EVIDENCE_PATH: str = str(

        EVIDENCE_DIR

    )


    EVENT_PATH: str = str(

        EVENT_DIR

    )







    class Config:

        env_file = (

            BASE_DIR

            /

            ".env"

        )


        extra = "ignore"








settings = Settings()