from pydantic import BaseModel
import uuid
from typing import Optional
from src.db.model import User, Book

class reviewmodel(BaseModel):
    uid:uuid.UUID
    rating:int 
    review:str
    user_id:uuid.UUID
    book_id:uuid.UUID
    user:Optional[User]
    book:Optional[Book]

class reviewcreatemodel(BaseModel):
    rating :int
    review:str