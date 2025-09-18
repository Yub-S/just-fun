# user model

from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class user(SQLModel,table=True):
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
    password_hash:str
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

