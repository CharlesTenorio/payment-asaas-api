from typing import Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.usuario import UsuarioModel
from schemas.usario_schema import UsuarioSchemaBase, UsuarioSchemaCreate
from core.deps import get_session, get_current_user
from core.security import create_hashed_password
from core.auth import autenticacar, create_access_token

router = APIRouter()

# GET usuario Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST Criar usuário
@router.post('/singup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def singup(usr: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UsuarioModel=UsuarioModel(nome=usr.nome, email=usr.email, senha=create_hashed_password(usr.senha))
    async with db as session:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

# GET usuário id
@router.get('/{usr_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_user(usr_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usr_id)
        result = await session.execute(query)
        usr: UsuarioModel = result.scalars().unique().one_or_none()
        if usr:
            return usr
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

# POST Login
@router.post('/login', response_model=UsuarioSchemaBase)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usr = await autenticacar(email=form_data.username, senha=form_data.password, db=db)
    if not usr:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário ou senha inválidos')
    return JSONResponse(content={"access_token": create_access_token(sub=usr.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)