from fastapi import APIRouter, status, Depends, HTTPException, Response
from model.compra_cartao import Cartao, CliCardHolderInfo, Costumer, ValorCompra
from model.usuario import UsuarioModel
from core.deps import get_session, get_current_user
from payment.pagamento import payment, GetClienteId, pagamento_pix

router = APIRouter()


@router.get("/api/v1/balance")
async def get_balance():
    return

@router.post("/api/v1/cliente")
async def NewClient(cli :Costumer):
    new_customer = GetClienteId(cli)  
    
    return  new_customer

@router.post("/api/v1/credito", status_code=status.HTTP_201_CREATED)
async def NewPayment(cli :Costumer, card: Cartao, cliCard: CliCardHolderInfo, valor: ValorCompra, usuario_logado: UsuarioModel = Depends(get_current_user)):
    pg = payment(cli, card, cliCard, valor)
    return pg


@router.post("/api/v1/pix", status_code=status.HTTP_201_CREATED)
async def Pix(cli :Costumer, valor: ValorCompra, usuario_logado: UsuarioModel = Depends(get_current_user)):
    result = pagamento_pix(cli, valor)
    return result
