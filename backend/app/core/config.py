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
# Works for:
# 1. Development
# 2. PyInstaller EXE
# ----------------------------------

def get_base_dir():



    exe_path = os.getenv(

        "HMEL_BASE_DIR"

    )



    if exe_path:



        return Path(

            exe_path

        )







    return Path(

        __file__

    ).resolve().parents[2]










BASE_DIR = get_base_dir()









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
    # ------------------------------

    STORAGE_PATH: str = "storage"



    MODEL_PATH: str = "storage/models"



    EVIDENCE_PATH: str = "storage/evidence"











    # ------------------------------
    # AI SETTINGS
    # ------------------------------

    CONFIDENCE_THRESHOLD: float = 0.4



    FRAME_SKIP: int = 5



    ALERT_COOLDOWN: int = 20












    # ------------------------------
    # Pydantic v2 config
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