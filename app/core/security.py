from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_password(password: str, hashed_password: str) -> bool:
    return CRIPTO.verify(password, hashed_password)

def create_hashed_password(password: str) -> str:
    return CRIPTO.hash(password)