import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY_ASAAS')

class Settings(BaseSettings):
   API_V1_STR: str = "/api/v1"
   API_KEY_ASAAS: str = api_key
   

settings = Settings()
