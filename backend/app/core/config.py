import os

from pathlib import Path

from functools import lru_cache



from pydantic_settings import (

    BaseSettings,

    SettingsConfigDict

)





# ----------------------------------
# Resolve Base Directory
#
# Development + PyInstaller
# ----------------------------------

def get_base_dir():


    exe_path = os.getenv(
        "HMEL_BASE_DIR"
    )


    if exe_path:


        return Path(
            exe_path
        )



    return (

        Path(__file__)

        .resolve()

        .parents[2]

    )






BASE_DIR = get_base_dir()







# ----------------------------------
# Resolve Storage Directory
#
# Priority:
# 1. Installer selected path
#    storage_config.txt
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









STORAGE_DIR = get_storage_dir()



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









# ----------------------------------
# Create Storage Folders
# ----------------------------------

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
# Environment File
# ----------------------------------

ENV_PATH = (

    BASE_DIR

    /

    ".env"

)









# ----------------------------------
# Application Settings
# ----------------------------------

class Settings(BaseSettings):



    # ------------------------------
    # APP
    # ------------------------------

    APP_NAME: str = "HMEL Vision Platform"



    ENVIRONMENT: str = "production"









    # ------------------------------
    # DATABASE
    # ------------------------------

    DATABASE_URL: str










    # ------------------------------
    # SECURITY
    # ------------------------------

    SECRET_KEY: str



    ALGORITHM: str = "HS256"



    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60











    # ------------------------------
    # STORAGE
    #
    # Generated dynamically
    # DO NOT put in .env
    # ------------------------------

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










    # ------------------------------
    # AI SETTINGS
    # ------------------------------

    CONFIDENCE_THRESHOLD: float = 0.4



    FRAME_SKIP: int = 5



    ALERT_COOLDOWN: int = 20











    # ------------------------------
    # Pydantic v2 Config
    # ------------------------------

    model_config = SettingsConfigDict(


        env_file=ENV_PATH,


        env_file_encoding="utf-8",


        extra="ignore"


    )











# ----------------------------------
# Cached Settings
# ----------------------------------

@lru_cache()

def get_settings():


    return Settings()







settings = get_settings()