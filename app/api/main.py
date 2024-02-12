from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from model.compra_cartao import Cartao, CliCardHolderInfo, Costumer, ValorCompra
from payment.pagamento import payment, GetClienteId

app = FastAPI()


@app.get("/api/v1/balance")
async def get_balance():
    return

@app.post("/api/v1/cliente")
async def NewClient(cli :Costumer):
    new_customer = GetClienteId(cli)  
    
    return  new_customer

@app.post("/api/v1/pagamento")
async def NewPayment(cli :Costumer, card: Cartao, cliCard: CliCardHolderInfo, valor: ValorCompra):
    pg = payment(cli, card, cliCard, valor)
    return pg


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)