from pydantic import BaseModel
import uuid 
from typing import Optional

class book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    user_uid: Optional[uuid.UUID] = None  # fix here
    language: str
    

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