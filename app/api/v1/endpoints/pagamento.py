from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from model.compra_cartao import Cartao, CliCardHolderInfo, Costumer, ValorCompra
from payment.pagamento import payment, GetClienteId, pagamento_pix
from core.config import settings
router = APIRouter()
security = HTTPBearer()


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
def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        if not payload.get("authorized"):
            raise HTTPException(status_code=403, detail="Não autorizado")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

@router.post("/credito", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def NewPayment(cli :Costumer, card: Cartao, cliCard: CliCardHolderInfo, valor: ValorCompra):
    pg = payment(cli, card, cliCard, valor)
    return pg


@router.post("/pix", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def Pix(cli :Costumer, valor: ValorCompra):
    result = pagamento_pix(cli, valor)
    return result
