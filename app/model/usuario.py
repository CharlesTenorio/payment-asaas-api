from sqlalchemy import Column, Integer, String
from core.config import settings

class UsuarioModel(settings.DBBASEModel):
    __tablename__ = "tb_usuarios"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), index=True,nullable=False, unique=True)
    senha: str = Column(String(255), nullable=False)