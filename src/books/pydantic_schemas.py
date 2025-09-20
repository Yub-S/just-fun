from pydantic import BaseModel
import uuid 

class book(BaseModel):
    uid:uuid.UUID
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    user_uid:uuid.UUID
    language:str
    

class createbook(BaseModel):
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str

class updatebook(BaseModel):
    title:str
    publisher:str
    page_count:int
    language:str