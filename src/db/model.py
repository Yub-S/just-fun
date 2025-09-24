from sqlmodel import SQLModel,Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import uuid
# from src.auth import model


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
    is_verified: bool = Field(
    sa_column=Column(pg.BOOLEAN, nullable=False, server_default="false")
)
    email:str
    password_hash:str=Field(exclude=True)
    role: str = Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})  # use string
    review:List["Review"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy": "selectin"})


    def __repr__(self,):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):

    __tablename__= "books"

    uid:uuid.UUID= Field(
        sa_column = Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str
    user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="user_accounts.uid")
    created_at:datetime = Field (sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="books",sa_relationship_kwargs={"lazy": "selectin"})
    review:List["Review"]=Relationship(back_populates="book",sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self,):
        return f"<Book {self.title}>"
    

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID, nullable=False,
        primary_key=True,
        default=uuid.uuid4
    )) 
    rating:int = Field(le=5)
    review:str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False
    ))
    user_id:uuid.UUID=Field(default=None, foreign_key="user_accounts.uid")
    book_id:uuid.UUID=Field(default=None, foreign_key="books.uid")
    created_at:datetime = Field(
        sa_column = Column(
            pg.TIMESTAMP, default=datetime.now
        )
    )
    user:Optional[User]=Relationship(back_populates="review",sa_relationship_kwargs={"lazy": "selectin"})
    book:Optional[Book]=Relationship(back_populates="review",sa_relationship_kwargs={"lazy": "selectin"})


