from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from fastapi import Request, status


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