from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    download_dir: str

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


settings = Settings()
