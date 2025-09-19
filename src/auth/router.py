from fastapi import APIRouter, Depends,status
from fastapi.exceptions import HTTPException
from src.auth.service import UserService
from datetime import timedelta, datetime
from src.auth.scheme import createuserdata,logindata, user
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.utils import verify_password_hash,create_access_token,decode_token
from fastapi.responses import JSONResponse
from src.auth.dependency import tokenbearer,accesstokenbearer,refreshtokenbearer
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
userservice = UserService()

# signup
@auth_router.post("/signup", response_model = user, status_code = status.HTTP_201_CREATED)
async def create_new_user(userdata:createuserdata, session:AsyncSession = Depends(get_session)):
    email = userdata.email
    user_exist = await userservice.user_exits(email,session)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user already exits")
    user_data =  await userservice.create_user(userdata,session)
    return user_data

# login 
@auth_router.post("/login")
async def login_users(login_data:logindata,session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await userservice.get_user_by_email(email,session)
    if user is not None:
        is_password_valid= verify_password_hash(password,user.password_hash)

        if is_password_valid:
            access_token = create_access_token(userdata = {
                "email":email,
                "user_uid":str(user.uid)
            })

            refresh_token = create_access_token(userdata = {
                "email":email,
                "user_uid":str(user.uid)
            },
            refresh=True,
            expiry=timedelta(days =1))


            return JSONResponse(
                content = {
                    "message":"login_successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{"email":user.email,"uid":str(user.uid)}
                }
            )
        
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "invalid email or password"
    )
        
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict=Depends(refreshtokenbearer())):
    expiry_date = token_details["exp"]

    if datetime.fromtimestamp(expiry_date) > datetime.now():
        new_access_token = create_access_token(token_details["user"])
        return JSONResponse (content = {"access_token" : new_access_token})
    
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST, details = "invalid or expired token"
    )


@auth_router.get("/logout")
async def revoke_token(token_details:dict=Depends(accesstokenbearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message":"logout succesfully"}, status_code=status.HTTP_200_OK)
