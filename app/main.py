from fastapi import FastAPI,Request,Response,status
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
from pydantic import BaseModel
import uvicorn
from random import randrange
from mysql.connector import connect
import sys
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Select
import os
from dotenv import load_dotenv

#Load environment values from .env file

class post_schema(BaseModel):
    title: str
    firstname: str
    lastname: str
    content: str

app = FastAPI()

#create engine for sqlalchemy
engine = create_engine("mysql+pymysql://root:redhat123@localhost/posts")

#create connection to mysql
conn = engine.connect()

#meta object to hold table metadata
posts_table_meta = MetaData()

posts_table = Table('posts',posts_table_meta,Column('id', Integer, primary_key=True, autoincrement=True),Column('title', String(255)),Column('firstname', String(255)),Column('lastname', String(255)),Column('content',String(255)))
posts_table_meta.create_all(engine)


def find_post_in_db(post_id):
    select_sql_where_instruction = posts_table.select().where(posts_table.c.id == post_id)
    exec_sql = conn.execute(select_sql_where_instruction).fetchone()
    if exec_sql == None:
        return {"msg": "Data not found"}
    return list(exec_sql)

@app.get("/")
async def users():
    return {
        "Hello": "World"
    }

@app.get("/list_posts")
def users():
    result_list = []
    select_sql_instruction = posts_table.select()
    exec_sql = conn.execute(select_sql_instruction).all()
    for row in exec_sql: 
        result_list = result_list + [list(row)] #Row is a tuple and can not be returned using return. Hence need to convert it to list
    return result_list

@app.get("/post/{passed_id}", status_code=status.HTTP_200_OK)
async def post_by_id(passed_id: int, status_code: Response):
    post = find_post_in_db(passed_id)
    return post
  
    
@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def create_item(post: post_schema):
    post_json = post.model_dump()
    insert_sql_statement = posts_table.insert().values(title=post_json['title'],firstname=post_json['firstname'],lastname=post_json['lastname'],content=post_json['content'])
    conn.execute(insert_sql_statement)
    commit = conn.commit()
    if commit == None:
        return {"msg": "Data inserted successfully"}
    else:
        return {"msg": "Data not inserted successfully"}

@app.delete("/delete/post/{passed_id}")
def delete_post(passed_id: int,status_code: Response):
    select_sql_instruction = posts_table.select().where(posts_table.c.id == passed_id)
    exec_sql = conn.execute(select_sql_instruction).fetchone()
    if exec_sql == None:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Post not found"}
    delete_sql_instruction = posts_table.delete().where(posts_table.c.id == passed_id)
    exec_delete_sql = conn.execute(delete_sql_instruction)
    delete_commit = conn.commit()
    if delete_commit != None:
        return {"msg": "Post Not deleted"}
    return {"msg": "Post Succesfully deleted"}

    
@app.put("/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int):
    post_json = post.model_dump()
    post = find_post_in_db(passed_id)
    update_post_sql = posts_table.update().where(posts_table.c.id == passed_id).values(title=post_json['title'],firstname=post_json['firstname'],lastname=post_json['lastname'],content=post_json['content'])
    conn.execute(update_post_sql)
    update_commit = conn.commit()
    print(update_commit)

@app.patch("/patch_post_title/{passed_id}",status_code=status.HTTP_200_OK)
async def patch(passed_id: int, request_patch: Request):
    sql_statements = []
    request_data = await request_patch.json() #contains the post body. Is a map. 

    for k,v in request_data.items():
        if k == "age":
            sql_statements = sql_statements +  [f'update posts set {k} = {v} where id={passed_id}']
        else:
            sql_statements = sql_statements +  [f'update posts set {k} = "{v}" where id={passed_id}']


    failed = 0

    for sql_query in sql_statements:
        print(sql_query)
        connection = connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),database=os.getenv('DB_NAME'),password="redhat123")
        cursor = connection.cursor()
        exec_result = cursor.execute(sql_query)

        if exec_result == None:
            connection.commit()
            cursor.close()
            connection.close()
            failed == 0
            continue 
        else:
            failed == 1
    
    if failed:
        return {
            "msg": "Error updating post"
        }
    else:
        return {
            "msg": "Post Updated fine"
        }
    






    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
