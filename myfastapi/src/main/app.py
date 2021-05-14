import uvicorn

from typing import List
from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.orm import Session

from src.users import crud, models
from src.users.schemas import UserSchema, UserCreateSchema, UserLoginSchema

from src.database import SessionLocal, engine

from src.auth.auth_hash import hash_password
from src.auth.auth_handler import signJWT
from src.auth.auth_schemas import TokenSchema

from src.utils.dependency import get_db

# Apply migrations to db and populate it
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# post /users/signup - rejestrowanie użytkownika
@app.post("/users/signup", tags=["user"], response_model=TokenSchema) # response_model=TokenSchema
def create_user(
        user: UserCreateSchema,
        db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=user)
    if user:
        return signJWT(user.email)


# user login
@app.post("/user/login", tags=["user"], response_model=TokenSchema)
async def user_login(
        user: UserLoginSchema = Body(...),
        db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user.hashed_password == hash_password(user.password):
        return signJWT(user.email)
    raise HTTPException(status_code=400, detail="Wrong login details!")

# get /users - lista użytkowników
@app.get("/users", tags=["user"], response_model=List[UserSchema])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# get /users/id - dane użytkownika
@app.get("/users/{user_id}", tags=["user"], response_model=UserSchema)
def read_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


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
    uvicorn.run("app:app", host='localhost', port=8000, reload=True)