from pydantic import BaseModel, Field
import uuid
from datetime import datetime

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
   