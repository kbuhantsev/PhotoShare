from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_db_name: str = "photo_share"
    postgres_domain: str = "localhost"
    postgres_port: str = "5432"

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # REDIS
    # redis_host: str = "localhost"
    # redis_port: int = 6379
    # redis_db: int = 0

    # # CLOUDINARY
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    cloudinary_folder: str = ""

    @staticmethod
    def get_db_uri():
        return f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_domain}:{settings.postgres_port}/{settings.postgres_db_name}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
