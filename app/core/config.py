from pydantic import BaseSettings, SecretStr, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    # Database settings
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    jwt_secret: str


    def get_database_url(self) -> str:
        # Construct the database URL using the settings
        DATABASE_URL = (
                f"postgresql+psycopg://"
                f"{self.DB_USER}:"
                f"{self.DB_PASSWORD.get_secret_value()}@"
                f"{self.DB_HOST}:"
                f"{self.DB_PORT}/"
                f"{self.DB_NAME}"
            )
        return DATABASE_URL


settings = Settings()