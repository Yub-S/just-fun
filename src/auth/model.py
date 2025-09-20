# user model

from sqlmodel import SQLModel,Field,Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import List
from src.db import model


class User(SQLModel,table=True):
    __tablename__= "user_accounts"

    uid:uuid.UUID=Field(
    sa_column=Column(
        pg.UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4
    ))
    username:str
    firstname:str
    lastname:str
    email:str
    password_hash:str=Field(exclude=True)
    role: str = Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    books: List["model.Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})  # use string


    def __repr__(self,):
        return f"<User {self.username}>"
