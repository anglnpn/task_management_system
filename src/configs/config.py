from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class AppSettings(BaseSetting):
    BASE_DIR: Path = BASE_DIR
    SERVICE_NAME: str
    SERVICE_VERSION: str
    API_VERSION: str
    ENVIRONMENT: str
    DEBUG: bool
    SERVICE_PORT: int
    EXTERNAL_SERVICE_SCHEMA: str = "http"
    EXTERNAL_SERVICE_HOST: str
    EXTERNAL_SERVICE_PORT: int
    SECRET_KEY_ADMIN: str = "default_secret"

    @property
    def full_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}:"
            f"{self.EXTERNAL_SERVICE_PORT}"
        )


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class RedisSetting(BaseSetting):
    REDIS_HOST: str
    REDIS_PORT: int


class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int


class MailSettings(BaseSetting):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True


class LogSettings(BaseSetting):
    LOG_FILE: str = "/logs/service.log"
    LOG_LEVEL: str = "DEBUG"


class AdminSettings(BaseSetting):
    ADMIN_FIRST_NAME: str = ("admin",)
    ADMIN_SECOND_NAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@gmail.com"


app_settings = AppSettings()
db_settings = DBSettings()
jwt_settings = JWTSettings()
log_settings = LogSettings()
redis_settings = RedisSetting()
mail_settings = MailSettings()
admin_settings = AdminSettings()
