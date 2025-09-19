from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from fastapi import Request, status, Depends
from typing import List
from src.db.main import get_session
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService

class tokenbearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self,request:Request)-> HTTPAuthorizationCredentials | None :
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = self.valid_token(token)

        if not token_data:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN, 
                detail = {"error":"this token is expired or invalid",
                          "resolution":"please get a new token"}
            )
        
        if await token_in_blocklist(token_data["jti"]) :
            raise HTTPException (
                status_code = status.HTTP_403_FORBIDDEN, 
                detail={"error":"this token is invalid or revoked",
                        "resolution":"create new access token"}
            )
        self.which_token(token_data)
        return token_data
    

    def valid_token(self,token:str)->bool:
        token_data = decode_token(token)
        return token_data 
    
    def which_token(self,token_data:dict):
        pass

class accesstokenbearer(tokenbearer):

    def which_token(self,token_data:dict):
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                detail="please provide access token")

class refreshtokenbearer(tokenbearer):

    def which_token(self,token_data:dict):
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                detail="please provide refresh token")

async def get_current_user(token_data:dict=Depends(accesstokenbearer()), session : AsyncSession=Depends(get_session)):

    user_data = await UserService().get_user_by_email(token_data["user"]["email"],session)
    return user_data

class RoleChecker:

    def __init__(self, allowed_roles:List[str])->None:
        self.allowed_roles = allowed_roles

    def __call__(self,current_user=Depends(get_current_user)):
        if current_user.role in self.allowed_roles :
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have access to perform this action because of RBAC."
        )
