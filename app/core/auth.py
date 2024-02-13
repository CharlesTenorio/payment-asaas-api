from pydantic import EmailStr
from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from model.usuario import UsuarioModel
from core.config import settings
from core.security import check_password

out2_schema = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{settings.API_V1_STR}/usr/login"
)

async def autenticacar (email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
   async with db as session:
       query = select(UsuarioModel).filter(UsuarioModel.email == email)
       result = await session.execute(query)
       usuario: UsuarioModel = result.scalars().unique().one_or_none()
       if not usuario:
           return None
       if not check_password(senha, usuario.senha):
           return None
       return usuario

def _create_access_token(type_token: str, time_life: timedelta, sub: str)-> str:
    payload = {}
    recife = timezone("America/Recife")
    expira = datetime.now(tz=recife) + time_life
    payload["type"]= type_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=recife)
    payload["sub"] = str(sub)
  
    return  jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(
    type_token="access_token",
    time_life=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    sub=1
    ):
    return _create_access_token(
        type_token=type_token,
        time_life=time_life,
        sub=sub
)
