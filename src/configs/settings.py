from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    download_dir: str
    azure_storage_connection_string: str | None = (
        None  # todo: split by domain (settings.azure.storage_connection_string...)
    )
    azure_storage_container_name: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def blob_enabled(self) -> bool:
        return (
            self.azure_storage_connection_string is not None
            and self.azure_storage_container_name is not None
        )


settings = Settings()
