from fastapi import FastAPI
from typing import Optional 
from pydantic import BaseModel
from fastapi import Header

app = FastAPI()

@app.get ("/")
async def read_root():
    return ({"message": "Hello, World!"})

# @app.get ("/greet/{name}")
# async def greet_name (name: str) -> dict : 
#     return ({"message" : f"Hello {name}"})

# query parameter
@app.get ("/greet")
async def greet_name (name : str)-> dict :
    return ({"message": f"Hello {name}"})

#mix both path and query parameter 
@app.get ("/greet/{name}") # any parameter not defined here is a query parameter
async def greet_name (name:str, codename:str)-> dict :
    return ({"message": f"Hello {name}, your codename is {codename}"})

# optional query parameter  - we can use Optional from typing module 
@app.get ("/welcome")
async def welcome (name:Optional[str]="User", codename:str="007")-> dict :
    return ({"message": f"welcome {name}, your codename is {codename}"})

class Book(BaseModel):
    title:str
    author:str

# post request - we need to validate or serialize the incoming data with pytantic model
@app.post("/create_book")
async def create_book(Book_data:Book):
    return ({"message": f"Book {Book_data.title} by {Book_data.author} created successfully !"})

# accessing request headers
@app.get("/get_headers") #,status_code=500 can also be set just show that we can explicitely state the status code here
async def get_headers(accept:str=Header(None),content_type:str=Header(None), user_agent:str=Header(None), host:str=Header(None)):
    header_dict = {}
    header_dict["accept"]=accept
    header_dict["user_agent"]=user_agent
    header_dict["content_type"]=content_type
    header_dict["host"]=host
    return header_dict
