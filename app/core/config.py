import os
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY_ASAAS')
token_jwt = os.getenv('JWT_SECRET_KEY')
class Settings(BaseSettings):
   API_V1_STR: str = "/api/v1"
   API_KEY_ASAAS: str = api_key
   USERNAME: str = os.getenv('USERNAME')
   PASSWORD: str = os.getenv('PASSWORD')
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 *24 * 7
   JWT_SECRET_KEY: str = token_jwt
   '''
     import secrets
     token : str = secrets.token_urlsafe(32)
     token
   '''
   ALGORITHM: str = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 *24 * 7
   
   class Config:
      case_sensitivity = True

settings : Settings = Settings()