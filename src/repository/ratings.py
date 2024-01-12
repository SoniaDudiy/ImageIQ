from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.conf import messages
from src.database.models import Rating, Image, User
from src.schemas.images import RatingModel


async def add_rating(
                     body: RatingModel,
                     image_id: int,
                     user: User,
                     db: Session
                     ) -> Rating:
    # Check if the image exists
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)

    # Check if the user is not the owner of the image
    if image.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=messages.CANNOT_RATE_OWN_IMAGE)

    # Check if the user has already rated the image
    existing_rating = db.query(Rating).filter(Rating.image_id == image_id, Rating.user_id == user.id).first()
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ALREADY_RATED)

    # Create a new rating
    rating = Rating(image_id=image_id, user_id=user.id, rating=body.rating)
    db.add(rating)
    db.commit()
    db.refresh(rating)

    return rating


async def get_ratings(
                image_id: int,
                db: Session
                ) -> List[Rating]:
    # Check if the image exists
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)

    # Get all ratings for the image
<<<<<<< Updated upstream
    ratings = db.query(Rating).filter(Rating.image_id == image_id).all() 
=======
    ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
>>>>>>> Stashed changes

    return ratings


async def remove_rating(
                         rating_id: int,
                         user: User,
                         db: Session
                         ) -> dict:
    # Check if the rating exists
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.RATING_NOT_FOUND)

    # Check if the user is the owner of the rating or an admin
    if rating.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=messages.NOT_AUTHORIZED)

    # Delete the rating
    db.delete(rating)
    db.commit()
<<<<<<< Updated upstream
=======
    db.refresh(image)
>>>>>>> Stashed changes

    return {'message': messages.RATING_DELETED}