from fastapi import APIRouter, Depends,status
from fastapi.exceptions import HTTPException
from src.auth.service import UserService
from src.auth.scheme import createuserdata, user
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

auth_router = APIRouter()
userservice = UserService()

@auth_router.post("/signup", response_model = user, status_code = status.HTTP_201_CREATED)
async def create_new_user(userdata:createuserdata, session:AsyncSession = Depends(get_session)):
    email = userdata.email
    user_exist = await userservice.user_exits(email,session)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user already exits")
    user_data =  await userservice.create_user(userdata,session)
    return user_data
