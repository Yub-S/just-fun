from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.model import Book
from datetime import datetime
from src.books.pydantic_schemas import createbook, updatebook

class BookService:
    """ This class will provide methods to create, read, update,delete books"""

    async def get_all_books(self,session:AsyncSession):

        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()
    
    async def get_a_book(self,book_uid:str,session:AsyncSession):

        statement = select(Book).where(Book.uid==book_uid)
        result = await session.exec(statement)

        book= result.first()
        return book if book is not None else None
    
    async def create_a_book(self, book_data:createbook, session:AsyncSession):

        book_data_dict = book_data.model_dump()
        new_book = Book(
            **book_data_dict
        )

        session.add(new_book)

        await session.commit()
        return new_book
    
    async def update_a_book(self,book_uid:str,update_data:updatebook, session:AsyncSession):

        book_to_update = await self.get_a_book(book_uid,session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k,v in update_data_dict.items():
                setattr(book_to_update,k,v)
            await session.commit()

            return book_to_update
        
        else:
            return None
        

    async def delete_a_book(self,book_uid:str,session:AsyncSession):

        book_to_delete = await self.get_a_book(book_uid,session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return None
