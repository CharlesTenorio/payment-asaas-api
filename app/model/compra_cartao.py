from core.config import settings
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Cartao(BaseModel):
     holderName: str
     number: str
     expiryYear: str
     expiryMonth: str
     ccv: str
   
class CliCardHolderInfo(BaseModel):
      name: str
      email: str
      cpfCnpj: str
      postalCode: str
      addressNumber: str
      addressComplement: str
      phone: str
   
class Costumer(BaseModel):
      name: str
      email: str
      cpfCnpj: str
   

class ValorCompra(BaseModel):
      valCompra: int
