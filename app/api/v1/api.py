from fastapi import APIRouter

from api.v1.endpoints import pagamento

api_router = APIRouter()

api_router.include_router(pagamento.router, prefix="/pagamento", tags=["pagamento"])
