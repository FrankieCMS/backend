"""FrankieCMS Configuartion File"""
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "FrankieCMS"
VERSION = "1.0.0"
ROUTER_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")
ACESS_TOKEN_ALGORITHM = config("ACESS_TOKEN_ALGORITHM", cast=str, default="CHANGEME")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default="CHANGEME"
)

ENVIRONMENT = config("APP_ENV", cast=str, default="DEVELOPMENT")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}\
:{POSTGRES_PORT}/{POSTGRES_DB}",
)

MAIL_USERNAME = config("MAIL_USERNAME", cast=str)
MAIL_PASSWORD = config("MAIL_PASSWORD", cast=str)
MAIL_FROM = config("MAIL_FROM", cast=str)
MAIL_PORT = config("MAIL_PORT", cast=int)
MAIL_SERVER = config("MAIL_SERVER", cast=str)
MAIL_FROM_NAME = config("MAIL_FROM_NAME", cast=str)
MAIL_TLS = config("MAIL_TLS", cast=bool, default=False)
MAIL_SSL = config("MAIL_SSL", cast=bool, default=False)
USE_CREDENTIALS = config("USE_CREDENTIALS", cast=bool, default=False)
VALIDATE_CERTS = config("VALIDATE_CERTS", cast=bool, default=False)
EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"
