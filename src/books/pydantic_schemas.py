from pydantic import BaseModel

class book(BaseModel):
    id:int
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