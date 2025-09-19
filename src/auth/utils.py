from passlib.context import CryptContext
from src.config import Config
import jwt
import uuid
import logging
from datetime import datetime, timedelta

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str)->str:
    return passwd_context.hash(password)

def verify_password_hash(password:str,hash:str)->bool:
    return passwd_context.verify(password,hash)


def create_access_token(userdata:dict,expiry:timedelta=None,refresh:bool=False):
    payload ={
        "user":userdata,
        "exp":datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti":str(uuid.uuid4()),
        "refresh":refresh
    }

    token = jwt.encode(payload=payload,
                       key = Config.JWT_KEY,
                       algorithm = Config.JWT_ALGORITHM
                       )
    return token

def decode_token(token)->dict:
    try :
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_KEY,
            algorithms=Config.JWT_ALGORITHM
        )
        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None