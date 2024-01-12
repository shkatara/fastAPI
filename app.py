from fastapi import FastAPI
from pydantic import BaseModel

class post_schema(BaseModel):
    title: str
    age: int

app = FastAPI()

@app.get("/")
def users():
    return {"Hello": "World"}

@app.get("/users")
def users():
    return {"testing": "data"}

@app.post("/post")
def create_item(post: post_schema):
    post_dictionary = post.dict()
    return post_dictionary