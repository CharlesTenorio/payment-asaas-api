from typing import Optional
from pydantic import BaseModel, EmailStr

class UsuarioSchemaBase(BaseModel):
    id: Optional[int]=None
    nome: str
    email: EmailStr
    
    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str