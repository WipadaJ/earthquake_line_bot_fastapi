from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# โหลดไฟล์ .env
load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    USER_DB_NAME: str
    DB_PASS: str

    LINE_CHANNEL_ACCESS_TOKEN: str
    LINE_CHANNEL_SECRET: str

    class Config:
        env_file = ".env"

# สร้าง instance ที่ใช้ได้ทั้งโปรเจกต์
settings = Settings()
