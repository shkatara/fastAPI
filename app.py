from fastapi import FastAPI,Request,Response,status
from pydantic import BaseModel
import uvicorn
from random import randrange

class post_schema(BaseModel):
    title: str
    age: int
    testingdata: str
    id: int

app = FastAPI()

content= [
    {
        "title": "FastAPI",
        "age":  10,
        "testingdata": "This is america",
        "id": 1
    },
    {
        "title": "NewWorld",
        "age":  20,
        "testingdata": "This is networking data",
        "id": 2
    },
    {
        "title": "Beautiful Python",
        "age":  30,
        "testingdata": "Learning to build API",
        "id": 3
    }
]

def find_post_by_id(passed_id):
    for data in content:
        if data['id'] == passed_id:
            return data
            

@app.get("/")
async def users():
    return {"Hello": "World"}

@app.get("/list_posts")
async def users():
    return content

@app.get("/post/{passed_id}")
async def post_by_id(passed_id: int, status_code: Response):
    post = find_post_by_id(passed_id)
    if not post:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {
            "msg": "Not Found",
            "status_code": status.HTTP_404_NOT_FOUND
        }
    return {
        "data": post,
        "status_code": status.HTTP_200_OK
    }

@app.post("/createpost")
async def create_item(post: post_schema):
    post_dictionary = post.model_dump()
    post_dictionary['id'] = randrange(0,1000000)
    content.append(post_dictionary)
    return {"msg": "data added successfully"}

if __name__ == "__main__":
    find_post_by_id(1)
    uvicorn.run(app, host="0.0.0.0", port=8000)
