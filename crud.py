from fastapi import FastAPI,status
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException


app = FastAPI()

# books  will be a list of books each with a dictionary indicating single book
books = [
     {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Algorithms and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2021-01-01",
        "page_count": 9282,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Head First HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English",
    },
]
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

@app.get("/books",response_model=List[book])
async def get_all_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(bookdata:book)->dict:
    # convert pydantic data into dictionary we use model_dump
    new_data = bookdata.model_dump()
    books.append(new_data)
    return new_data

@app.get("/book/{book_id}")
async def get_a_single_book(book_id:int)->dict:
    for book in books:
        if book_id == book["id"]:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail= "book with that id not found"
                         )

@app.patch("/book/{book_id}")
async def update_record_of_a_book(book_id:int, newdetails:updatebook)-> dict:
    for book in books:
        if book_id==book["id"]:
            book["title"]=newdetails.title
            book["publisher"]=newdetails.publisher
            book["page_count"]=newdetails.page_count
            book["language"]=newdetails.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found that book")        

# remove/delete a book
@app.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def remove_a_book(book_id:int):
    for book in books:
        if book_id==book["id"]:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no content found")