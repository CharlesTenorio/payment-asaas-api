from asaas.payments import CreditCard, CreditCardHolderInfo, BillingType
from core.config import settings
from model.compra_cartao import Cartao, CliCardHolderInfo, Costumer, ValorCompra
from datetime import date
from asaas import Asaas

asaas = Asaas(
    access_token= settings.API_KEY_ASAAS,
    production = False
)
def GetClienteId(cli :Costumer):
    new_customer = asaas.customers.new(
        name = cli.name,
        email = cli.email,
        cpfCnpj = cli.cpfCnpj
    )

    return new_customer

def payment(cli :Costumer, card: Cartao, cliCard: CliCardHolderInfo, totalCompra: ValorCompra):
    
    new_customer = GetClienteId(cli)
    credit_card = CreditCard(
            holderName = card.holderName,
            number = card.number,
            expiryYear = card.expiryYear, 
            expiryMonth =card.expiryMonth,
            ccv = card.ccv
        )

    credit_card_holder_info = CreditCardHolderInfo(
            name = cliCard.name,
            email = cliCard.email,
            cpfCnpj = cliCard.cpfCnpj,
            postalCode = cliCard.postalCode,
            addressNumber = cliCard.addressNumber,
            addressComplement = cliCard.addressComplement,
            phone = cliCard.phone
        )

    pagamento = asaas.payments.new(
        customer = new_customer,
        billingType = BillingType.CREDIT_CARD,
        value = totalCompra.valCompra,
        dueDate = date.today(),
        creditCard = credit_card.json(),
        creditCardHolderInfo = credit_card_holder_info.json()
    )

    return pagamento
    
    
    
    
    