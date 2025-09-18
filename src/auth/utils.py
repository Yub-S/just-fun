from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str)->str:
    return passwd_context.hash(password)

def verify_password_hash(password:str,hash:str)->bool:
    return passwd_context.verify(password,hash)