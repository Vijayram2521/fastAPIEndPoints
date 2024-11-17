import os
from dotenv import load_dotenv

load_dotenv()


def get_env(variable_name, default=None):
    value = os.getenv(variable_name, default)
    if value and str(value).lower() in ("true", "false"):
        return str(value).lower() == "true"
    return value


# Postgres
DB_HOST="localhost"
DB_NAME="postgres"
DB_USER="myuser"
DB_PASSWORD="mypassword"

DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
