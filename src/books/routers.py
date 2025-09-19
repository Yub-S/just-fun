from fastapi import status, APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from typing import List
from .pydantic_schemas import book,createbook,updatebook
from .books_data import books
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependency import accesstokenbearer , RoleChecker

book_router = APIRouter()
book_service = BookService()
accesstokenbearer = accesstokenbearer()
role_checker= RoleChecker(["admin"])

# dependencies can be kept in the function below the router or within the routers
# in router -> dependencies=[list of dependencies] and in function Depends()
# as a role based access lets simply implement that only admin can upload the books contents not users

@book_router.get("/",response_model=List[book])
async def get_all_books(session:AsyncSession=Depends(get_session),token_details=Depends(accesstokenbearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=book, dependencies=[Depends(role_checker)])
async def create_a_book(bookdata:createbook,session:AsyncSession=Depends(get_session),token_details=Depends(accesstokenbearer))->dict:
    new_book = await book_service.create_a_book(bookdata,session)
    return new_book

@book_router.get("/{book_uid}",response_model=book)
async def get_a_single_book(book_uid:str,session:AsyncSession=Depends(get_session), token_details=Depends(accesstokenbearer))->dict:
    book = await book_service.get_a_book(book_uid,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "book with that id not found"
                            )

@book_router.patch("/{book_uid}",response_model =book)
async def update_record_of_a_book(book_uid:str, newdetails:updatebook,session:AsyncSession=Depends(get_session), token_details=Depends(accesstokenbearer))-> dict:
    updated_book = await book_service.update_a_book(book_uid, newdetails,session)
    if updated_book :
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found that book")        

# remove/delete a book
@book_router.delete("/{book_uid}",status_code=status.HTTP_200_OK)
async def remove_a_book(book_uid:str,session:AsyncSession=Depends(get_session), token_details=Depends(accesstokenbearer)):

    response = await book_service.delete_a_book(book_uid,session)
    if response :
       return {"message": "Deleted"}
    else:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no content found")