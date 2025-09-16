from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from .pydantic_schemas import book,updatebook
from .books_data import books

book_router = APIRouter()


@book_router.get("/",response_model=List[book])
async def get_all_books():
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(bookdata:book)->dict:
    # convert pydantic data into dictionary we use model_dump
    new_data = bookdata.model_dump()
    books.append(new_data)
    return new_data

@book_router.get("/{book_id}")
async def get_a_single_book(book_id:int)->dict:
    for book in books:
        if book_id == book["id"]:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail= "book with that id not found"
                         )

@book_router.patch("/{book_id}")
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
@book_router.delete("/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def remove_a_book(book_id:int):
    for book in books:
        if book_id==book["id"]:
            books.remove(book)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no content found")