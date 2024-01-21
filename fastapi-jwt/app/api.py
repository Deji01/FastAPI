from app.model import PostSchema, UserSchema, UserLoginSchema
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

from fastapi import FastAPI, Body, Depends
from typing import List, Dict

app = FastAPI()

posts = [{"id": 1, "title": "Pancake", "content": "Lorem Ipsum..."}]

users = []


def check_user(data: UserLoginSchema):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            return True
    return False


@app.get("/", tags=["root"])
async def read_root() -> Dict[str, str]:
    return {"message": "welcome to the blog!"}


@app.get("/posts", response_model=Dict[str, List[PostSchema]], tags=["posts"])
def get_posts():
    return {"data": posts}


@app.get("/posts/{id}", response_model=Dict[str, PostSchema], tags=["posts"])
def get_single_post(id: int):
    if id > len(posts):
        return {"error": f"Post with {id} doesn't exist."}
    result = [{"data": post} for post in posts if post["id"] == id]
    return result[0]


@app.post(
    "/posts",
    dependencies=[Depends(JWTBearer())],
    response_model=Dict[str, str],
    tags=["posts"],
)
def add_post(post: PostSchema):
    posts.append(post)
    return {"data": "post added."}


@app.post("/user/signup", response_model=Dict[str, str], tags=["user"])
def create_user(user: UserSchema):
    users.append(user)
    return signJWT(user["email"])


@app.post("/user/login", response_model=Dict[str, str], tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "wrong login details!"}
