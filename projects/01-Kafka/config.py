from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    BOOTSTRAP_SERVER : str
    SASL_MECHANISM: str
    SECURITY_PROTOCOL: str
    SASL_USERNAME: str
    SASL_PASSWORD: str
    SCHEMA_BOOTSTRAP_SERVER: str
    SCHEMA_USERNAME: str
    SCHEMA_PASSWORD: str
    OCI_SECRET_KEY : str
    OCI_ACCESS_KEY : str
    OCI_NAMESPACE   : str
    OCI_BUCKET     : str
    OCI_REGION     : str
    ADB_USER        : str
    ADB_PASSWORD    : str
    ADB_DSN         : str
    WALLET_DIR     : str
    LOCAL_TMP      : str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()