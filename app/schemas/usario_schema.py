from typing import Optional
from pydantic import BaseModel as SCBaseModel, EmailStr

class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int]=None
    nome: str
    email: EmailStr
    
    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str