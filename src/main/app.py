from typing import List

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.auth import JWTBearer, hash_password, sign_jwt
from src.crud import crud_movies, crud_rates, crud_user
from src.database import db_base, db_engine, db_session, get_db
from src.models import Movie, Rating, User
from src.schemas.movie import MovieSchema
from src.schemas.rating import RatingCreateSchema, RatingSchema
from src.schemas.user import (UserCreateSchema, UserLoginSchema, UserSchema,
                              UserTokenizedSchema)

# Apply migrations to db and populate it
db_base.metadata.create_all(bind=db_engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup", tags=["user"], response_model=UserTokenizedSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    """POST: Register new user"""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    new_user = crud_user.create_user(db=db, new_user=user)
    if new_user:
        token = sign_jwt(new_user.email).access_token
        user = {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
        }
        return UserTokenizedSchema(user=user, access_token=token)
        # return signJWT(new_user.email)


@app.post("/login", tags=["user"], response_model=UserTokenizedSchema)
async def user_login(
    user: UserLoginSchema = Body(...),
    db: Session = Depends(get_db)
):
    # """ GET: Return all user """
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        if db_user.hashed_password == hash_password(user.password):
            token = sign_jwt(user.email).access_token
            user = {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
            }
            return UserTokenizedSchema(user=user, access_token=token)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong login details!"
    )


@app.get("/users", tags=["user"], response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET: Return all user with pagination arguments"""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", tags=["user"], response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """GET: Return specific user by id"""
    db_user = crud_user.get_payload(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@app.get("/ratings/", tags=["ratings"], response_model=List[RatingSchema])
def read_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud_rates.get_ratings(db)
    return ratings


@app.get("/movies/", tags=["movies"], response_model=List[MovieSchema])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud_movies.get_movies(db=db, skip=skip, limit=limit)
    return movies


@app.get("/movies/{searchStr}", tags=["movies"], response_model=List[MovieSchema])
def search_movies(search_str: str, db: Session = Depends(get_db)):
    movies = crud_movies.search_movies_by_title(db=db, search_string=search_str)
    return movies

@app.get("/movies_vote/{searchStr}", tags=["movies"], response_model=List[MovieSchema])
def search_movies_with_rate(
        search_str: str,
        db: Session = Depends(get_db),
        # token_object: JWTBearer = Depends(JWTBearer())
):
    # payload = token_object.get_payload()
    # user_email = payload['user_id']
    # user = crud_user.get_user_by_email(db, user_email)
    # movies = crud_movies.search_movies_by_title_with_rate(db=db, search_string=search_str, user_id=user.id)


    # movies = db.query(Rating).join(User).all()
    # movies = db.query(Rating).join(User).filter(User.id == 1).all()
    #
    # movies = db.query(Movie).join(Rating).all()
    st1 = db.query(Movie).join(Rating).filter(Rating.user_id == 1).all()


    # .filter(Movie.title.contains('toy'))\
    # .join(Rating.rating, and_(Rating.movie_id == Movie.id, Rating.user_id == 1))\
    my_user_id = 1
    st2 = db.query(Movie)\
        .outerjoin(Rating, Rating.user_id == my_user_id)\
        .all()

    st3 = db.query(Movie).join(Rating, Rating.user_id == my_user_id, isouter=True).all()
    st4 = db.query(Movie).join(Rating).filter(Rating.user_id == my_user_id).all

    query = db.query(Movie.title, Rating.rating).outerjoin(Rating, Rating.user_id == my_user_id)
    query2 = db.query(Movie.title, Rating.rating).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
    query25 = db.query(Movie.id, Movie.imdb_id, Movie.title, Movie.genres, Movie.release_date, Movie.overview, Movie.vote_count, Movie.vote_average, Rating.rating.label('user_rate')).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
    query3 = db.query(Movie, Rating.rating).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
    query35 = db.query(Movie, Rating.rating.label('user_rate')).outerjoin(Rating, and_(Rating.movie_id == Movie.id, Rating.user_id == my_user_id))
    query4 = db.query(Movie).outerjoin(Rating, Rating.user_id == my_user_id)

    q1 = query.all()
    q2 = query2.all()
    q25 = query25.all()
    q3 = query3.all()
    q35 = query35.all()
    q4 = query4.all()
    # .filter(Rating.user_id == my_user_id)\

    xx = st3 #[1].ratings

    return q25


@app.post("/movies/rate/", tags=["ratings"], response_model=RatingSchema)
def rate_movie(req_rating: RatingCreateSchema, db: Session = Depends(get_db)):
    return crud_rates.apply_user_rating(db=db, req_rating=req_rating)


@app.get("/test", tags=["test"])
async def test_get_no_protected():
    return {"dump": "GET: no protected dump"}


@app.post("/test", tags=["test"])
async def test_post_no_protected():
    return {"dump": "POST: no protected dump"}


@app.get("/protected", dependencies=[Depends(JWTBearer())], tags=["test"])
async def test_protected():
    return {"dump": "GET: something protected"}


@app.get("/protected/user", tags=["test"])
async def test_protected_user(token_object : JWTBearer = Depends(JWTBearer())):
    payload = token_object.get_payload()
    return {"decrypted_user": payload}


@app.post("/protected", dependencies=[Depends(JWTBearer())], tags=["test"])
async def test_protected():
    return {"dump": "POST: something protected"}


if __name__ == "__main__":
    # uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_HOST_PORT)
    uvicorn.run("app:app", host="localhost", port=5000, reload=True, log_level="info")
