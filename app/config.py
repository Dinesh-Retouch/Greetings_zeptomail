from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ZEPTOMAIL_API_KEY: str
    ZEPTOMAIL_API_URL: str
    ZEPTOMAIL_SENDER_EMAIL: str
    ZEPTOMAIL_SENDER_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
