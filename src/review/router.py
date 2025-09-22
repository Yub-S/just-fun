from fastapi import APIRouter, Depends
from src.auth.dependency import get_current_user
from src.review.schema import reviewcreatemodel
from src.db.main import get_session
from src.review.service import ReviewService

review_service = ReviewService()
review_router = APIRouter()

@review_router.post("/book/{book_uid}")
async def add_review(book_uid:str,
                    review_data:reviewcreatemodel,
                    current_user=Depends(get_current_user),
                    session=Depends(get_session)
                     ):
    
    user_email = current_user.email
    review_data = await review_service.create_a_review(user_email,book_uid,review_data,session)
    return review_data


@review_router.get("/")
async def get_reviews(session=Depends(get_session)):
    reviews = await review_service.get_all_reviews(session)
    return reviews
