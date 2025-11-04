from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MOCK_DUTS: bool = False
    DEVICE_FILTERS: str | None = None  # "vid:pid,vid:pid" (hex, no 0x)
    LOG_DIR: str = "./data/logs"
    SERIAL_BAUD: int = 115200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
