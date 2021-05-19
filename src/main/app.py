from typing import List

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.auth.auth_bearer import JWTBearer
from src.auth.auth_handler import hash_password, signJWT
from src.database import db_base, db_engine, get_db, session_local

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


@app.post("/signup", tags=["user"], response_model=schemas.user.UserTokenizedSchema)
def create_user(user: schemas.user.UserCreateSchema, db: Session = Depends(get_db)):
    """POST: Register new user"""
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    new_user = crud.user.create_user(db=db, new_user=user)
    if new_user:
        token = signJWT(new_user.email).access_token
        user = {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
        }
        return schemas.user.UserTokenizedSchema(user=user, access_token=token)
        # return signJWT(new_user.email)


@app.post("/login", tags=["user"], response_model=schemas.user.UserTokenizedSchema)
async def user_login(
    user: schemas.user.UserLoginSchema = Body(...), db: Session = Depends(get_db)
):
    # """ GET: Return all user """
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        if db_user.hashed_password == hash_password(user.password):
            token = signJWT(user.email).access_token
            user = {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
            }
            return schemas.user.UserTokenizedSchema(user=user, access_token=token)
    raise HTTPException(tatus_code=status.HTTP_400_BAD_REQUEST, detail="Wrong login details!")


@app.get("/users", tags=["user"], response_model=List[schemas.user.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET: Return all user with pagination arguments"""
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", tags=["user"], response_model=schemas.user.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """GET: Return specific user by id"""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user

@app.get("/ratings/", tags=["ratings"], response_model=List[schemas.rating.Rating])
def read_ratings(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    ratings = crud.rates.get_ratings(db)
    return ratings


# @app.post("/users/{user_id}/rating/", response_model=schemas.Item)
# def create_item_for_user(
#         user_id: int,
#         item: schemas.ItemCreate,
#         db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/test", tags=["test"])
async def test_get_no_protected():
    return {"data": "GET: no protected data"}


@app.post("/test", tags=["test"])
async def test_post_no_protected():
    return {"data": "POST: no protected data"}


@app.get("/protected", dependencies=[Depends(JWTBearer())], tags=["test"])
async def test_protected():
    return {"data": "GET: something protected"}


@app.post("/protected", dependencies=[Depends(JWTBearer())], tags=["test"])
async def test_protected():
    return {"data": "POST: something protected"}


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#         user_id: int,
#         item: schemas.ItemCreate,
#         db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(
#         skip: int = 0,
#         limit: int = 100,
#         db: Session = Depends(get_db)
# ):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


if __name__ == "__main__":
    # uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_HOST_PORT)
    uvicorn.run("app:app", host="localhost", port=5000, reload=True, log_level="info")
