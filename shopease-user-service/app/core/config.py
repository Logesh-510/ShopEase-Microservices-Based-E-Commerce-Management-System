from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    APP_NAME: str = "ShopEase User Management Service"
    APP_ENV: str = "development"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "shopease_user_db"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    AUTH_SERVICE_URL: str = "http://127.0.0.1:8002"
    AUTH_VERIFY_TIMEOUT_SECONDS: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            drivername="mysql+pymysql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        )


settings = Settings()