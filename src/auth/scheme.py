from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.books.pydantic_schemas import book

class user(BaseModel):
    uid:uuid.UUID
    username:str
    firstname:str
    lastname:str
    email:str
    password_hash:str

class createuserdata(BaseModel):
    username:str=Field(max_length=25)
    firstname:str=Field(max_length=25)
    lastname:str=Field(max_length=25)
    email:str=Field(max_length=25)
    password:str=Field(min_length=8)
   
class logindata(BaseModel):
    email:str=Field(max_length=25)
    password:str=Field(min_length=8)

# class Usermodel(BaseModel):
#     uid:uuid.UUID
#     username:str
#     firstname:str
#     lastname:str
#     email:str
#     password_hash:str
#     role: str 
#     created_at:datetime

class UserBookModel(user):
    books:List[book]

class EmailModel(BaseModel):
    address:List[str]

class Passwordreset(BaseModel):
    email:str

class NewPassword(BaseModel):
    new_password:str
    confirm_new_password:str