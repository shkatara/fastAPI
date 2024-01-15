from fastapi import FastAPI,Request,Response,status
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
from pydantic import BaseModel
import uvicorn
from random import randrange

class post_schema(BaseModel):
    title: str
    age: int
    testingdata: str
    #id: int

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
            return data,content.index(data)
            

@app.get("/")
async def users():
    return {"Hello": "World"}

@app.get("/list_posts")
async def users():
    return content

@app.get("/post/{passed_id}", status_code=status.HTTP_200_OK)
async def post_by_id(passed_id: int, status_code: Response):
    post = find_post_by_id(passed_id)
    if not post:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {
            "msg": "Not Found",
            "status_code": status.HTTP_404_NOT_FOUND
        }
    return post[0]

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def create_item(post: post_schema):
    post_dictionary = post.model_dump()
    post_dictionary['id'] = randrange(0,1000000)
    content.append(post_dictionary)
    return {"msg": "data added successfully"}

@app.delete("/delete/post/{passed_id}")
def delete_post(passed_id: int):
    post = find_post_by_id(passed_id)
    if not post:
        return {
            "msg": "post not found",
            "status_code": status.HTTP_404_NOT_FOUND
        }
    content.remove(post)
    return content

@app.put("/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int):
    find_index = find_post_by_id(passed_id)
    post_index = find_index[1]
    content[post_index] = post.model_dump()
    content[post_index]['id'] = passed_id
    return content

@app.patch("/patch_post_title/{passed_id}",status_code=status.HTTP_200_OK)
async def patch(passed_id: int, request_patch: Request):
    find_index = find_post_by_id(passed_id)
    post_index = find_index[1]
    request_data = await request_patch.json()
    for k,v in request_data.items():
        if k == "title":
            content[post_index]['title'] =  request_data['title']
        if k == "age":
            content[post_index]['age'] =  request_data['age']
        if k == "testingdata":
            content[post_index]['testingdata'] =  request_data['testingdata']
    return content[post_index]

if __name__ == "__main__":
    find_post_by_id(1)
    uvicorn.run(app, host="0.0.0.0", port=8080)
