import redis.asyncio as redis
from src.config import Config

jti_expiry = 3600

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,port=Config.REDIS_PORT, db=0, decode_responses=True
)

async def add_jti_to_blocklist(jti:str)->None:
    await token_blocklist.set(name=jti,value="",ex=jti_expiry)

async def token_in_blocklist(jti:str)->bool:
    jti = await token_blocklist.get(jti)

    return jti is not None