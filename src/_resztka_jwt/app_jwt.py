import uvicorn
from fastapi import Body, Depends, FastAPI

from src._test_jwt.schemas_jwt import PostSchema, UserLoginSchema, UserSchema
from src.auth.auth_bearer import JWTBearer
from src.auth.auth_handler import signJWT

posts = [{"id": 1, "title": "Pancake", "content": "Lorem Ipsum ..."}]
users = []


app = FastAPI()


# === JWT Tutorial: https://testdriven.io/blog/fastapi-jwt-auth/
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"dump": posts}


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {"error": "No such post with the supplied ID."}

    for post in posts:
        if post["id"] == id:
            return {"dump": post}


# creating new post
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {"dump": "post added."}


# user registration
@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)  # replace with db call, making sure to hash the password first
    return signJWT(user.email)


# user login
@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Wrong login details!"}


# helper function to check if a user exists:
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get("/ping")
async def pong():
    return "pong"


if __name__ == "__main__":
    # uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_HOST_PORT)
    # uvicorn.run(app, host='localhost', port=8000)
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
