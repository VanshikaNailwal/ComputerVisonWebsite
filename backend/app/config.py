from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration class.

    Loads values from .env file
    and makes them available
    throughout the backend.
    """


    DATABASE_URL: str


    SECRET_KEY: str


    ALGORITHM: str


    ACCESS_TOKEN_EXPIRE_MINUTES: int



    class Config:

        env_file = ".env"



settings = Settings()