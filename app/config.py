from pydantic import BaseSettings


class Settings(BaseSettings):
    algorithm: str
    access_token_expire_minutes: int
    secret_key : str

    class Config:
        env_file = ".env"


settings = Settings()
