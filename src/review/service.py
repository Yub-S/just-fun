from src.review.schema import reviewcreatemodel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from sqlmodel import select, desc
from src.auth.service import UserService
from fastapi.exceptions import HTTPException
from src.db.model import Review
from fastapi import status

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def create_a_review(self,
                            user_email: str,
                            book_uid: str,
                            review_data: reviewcreatemodel,
                            session: AsyncSession):
        user = await user_service.get_user_by_email(user_email, session)
        book = await book_service.get_a_book(book_uid, session)

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="book not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user not found")

        review_data_dict = review_data.model_dump()
        new_review = Review(
            **review_data_dict,
            user_id=user.uid,
            book_id=book.uid
        )

        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)  # so you get uid, timestamps, etc.

        return new_review

    
    async def get_all_reviews(self,session:AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)
        return result.all()
    
    async def get_a_review(self,review_uid:str,session:AsyncSession):
        statement = select(Review).where(Review.uid==review_uid)
        result = await session.exec(statement)
        return result.first()
