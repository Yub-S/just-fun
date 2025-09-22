from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.scheme import createuserdata
from src.db.model import User
from src.auth.utils import generate_password_hash


class UserService:

    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement = select(User).where(User.email==email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def user_exits(self,email:str,session:AsyncSession):
        user = await self.get_user_by_email(email,session)
        return True if user is not None else False
    
    async def create_user(self,userdata:createuserdata,session:AsyncSession):

        user_data_dict = userdata.model_dump()
        new_user_data = User(
            **user_data_dict
        )
        new_user_data.password_hash = generate_password_hash(user_data_dict["password"])
        session.add(new_user_data)
        await session.commit()
        return new_user_data