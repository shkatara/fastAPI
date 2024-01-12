from fastapi import FastAPI
from pydantic import BaseModel

class post_schema(BaseModel):
    title: str
    age: int

app = FastAPI()
content= {"Hello": "World"}

@app.get("/")
async def users():
    return {"Hello": "World"}

@app.get("/users")
async def users():
    return {"testing": "data"}

@app.post("/post")
async def create_item(post: post_schema):
    post_dictionary = post.model_dump()
    
    return "Title is {} and Age is {} and content is {}".format(post_dictionary['title'],post_dictionary['age'],content)
