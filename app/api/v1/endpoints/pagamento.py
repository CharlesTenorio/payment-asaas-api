from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from model.compra_cartao import Cartao, CliCardHolderInfo, Costumer, ValorCompra
from payment.pagamento import payment, pagamento_pix
from core.config import settings


router = APIRouter()
security = HTTPBearer()

# Função para verificar o token JWT
def verify_token(token: str = Depends(security)):
    try:
        # Verifica se o token está presente nos cabeçalhos da requisição
        if not "Bearer" in token.scheme:
            raise HTTPException(status_code=403, detail="Token não fornecido corretamente")

        # Extrai o token da string "Bearer <token>"
        token_value = token.credentials

        # Decodifica o token JWT e verifica sua validade
        payload = jwt.decode(token_value, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        # Verifica se o token expirou
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=403, detail="Token expirado")

        # Verifica se o token contém a chave "access_token" e se é verdadeira
        if  payload["authorized"]==False:
            raise HTTPException(status_code=403, detail="Token inválido")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifica as credenciais do usuário (isso pode ser autenticação no banco de dados ou qualquer outro método de verificação)
    if form_data.username == settings.USERNAME and form_data.password == settings.PASSWORD:
        # Define as informações a serem incluídas no token JWT
        token_data = {
            "sub": form_data.username,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "authorized": True
        }
        # Gera o token JWT
        token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    else:
        # Se as credenciais estiverem incorretas, retorna um erro de não autorizado
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Verificação do token JWT


@router.post("/credito", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def NewPayment(cli :Costumer, card: Cartao, cliCard: CliCardHolderInfo, valor: ValorCompra):
    pg = payment(cli, card, cliCard, valor)
    return pg


@router.post("/pix", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def Pix(cli :Costumer, valor: ValorCompra):
    result = pagamento_pix(cli, valor)
    return result
