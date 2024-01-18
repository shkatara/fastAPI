from fastapi import FastAPI,Request,Response,status
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
from pydantic import BaseModel
import uvicorn
from random import randrange
from mysql.connector import connect
import sys

import os
from dotenv import load_dotenv

#Load environment values from .env file
load_dotenv()

#Connect to mysql database
connection = connect(
    host=os.getenv('DB_HOST'), 
    user=os.getenv('DB_USER'),
    database=os.getenv('DB_NAME'),
    password="redhat123" #Not the greatest idea to put password in plain text but for some reason os.getenv('DB_PASSW') is reading the password but the function
    #is not accepting it.
)

if not connection:
    sys.exit("Database not initialized. Exited...!!!")

#Create database cursor
conn = connection.cursor()



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

def find_post_in_db(*args):
    final_results = []
    if len(args) != 0:
        query = f'select * from {os.getenv("DB_TABLE_NAME")} where id={args[0]}'
    else:
        query = f'select * from {os.getenv("DB_TABLE_NAME")}'
    query_execute = conn.execute(query) 
    result = conn.fetchall()
    if result != 0:
        for data in result:
            final_results = final_results + [
            {
                "title": data[1],
                "First Name": data[3],
                "Last name": data[4],
                "content": data[5]
            }  ]
    else:
        return {
            "msg":"No Post Found"
        }
    return final_results

@app.get("/")
async def users():
    return {"Hello": "World"}

@app.get("/list_posts")
async def users():
    final_results = find_post_in_db()
    return final_results

@app.get("/post/{passed_id}", status_code=status.HTTP_200_OK)
async def post_by_id(passed_id: int, status_code: Response):
    final_results = find_post_in_db(passed_id)
    if len(final_results) != 0:
        return final_results
    else:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {
            "msg":"No Post Found"
        }

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def create_item(post: post_schema):
    post_dictionary = post.model_dump()
    post_dictionary['id'] = randrange(0,1000000)
    content.append(post_dictionary)
    return {
        "msg": "data added successfully"
        }

@app.delete("/delete/post/{passed_id}")
def delete_post(passed_id: int,status_code: Response):
    find_index = find_post_by_id(passed_id)

    if find_index == None:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {
            "msg": "post not found",
            "status_code": status_code.status_code
        }
    else:
        content.remove(find_index[0])
        return content
    
@app.put("/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int):
    find_index = find_post_by_id(passed_id)

    if find_index == None:
        return {
            "msg": "Post not found"
        }
        
    else:
        post_index = find_index[1]
        content[post_index] = post.model_dump()
        content[post_index]['id'] = passed_id
        return content[post_index]

@app.patch("/patch_post_title/{passed_id}",status_code=status.HTTP_200_OK)
async def patch(passed_id: int, request_patch: Request):
    find_index = find_post_by_id(passed_id)
    request_data = await request_patch.json()

    if find_index == None:
        status_code = status.HTTP_404_NOT_FOUND
        return {"msg":"Post not found"}
    else:
        post_index = find_index[1]
        for k,v in request_data.items():
            if k == "title":
                content[post_index]['title'] =  request_data['title']
            if k == "age":
                content[post_index]['age'] =  request_data['age']
            if k == "testingdata":
                content[post_index]['testingdata'] =  request_data['testingdata']
        return content[post_index]
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
