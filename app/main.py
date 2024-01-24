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


def find_post_in_db(*args):
    connection = connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),database=os.getenv('DB_NAME'),password="redhat123")
    if not connection:
        sys.exit("Database not initialized. Exited...!!!")

    cursor = connection.cursor()
    final_results = []
    if len(args) != 0:
        query = f'select * from {os.getenv("DB_TABLE_NAME")} where id={args[0]}'
    else:
        query = f'select * from {os.getenv("DB_TABLE_NAME")}'
    query_execute = cursor.execute(query) 
    result = cursor.fetchall()
    if result != 0:
        for data in result:
            final_results = final_results + [
            {
                "title": data[1],
                "First Name": data[3],
                "Last name": data[4],
                "content": data[5]
            }  ]
        cursor.close()
        connection.close()

    else:
        cursor.close()
        connection.close()
        return {
            "msg":" No Post Found"
        }
    return final_results

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
    #Create database connection
    connection = connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),database=os.getenv('DB_NAME'),password="redhat123")
    #Check if connection
    if not connection:
        sys.exit("Database not initialized. Exited...!!!")
    #create cursor
    cursor = connection.cursor()
    #Create query
    query = f'DELETE FROM {os.getenv("DB_TABLE_NAME")} where id={passed_id}'
    #run query
    exec_result = cursor.execute(query)
    #return exec_result
    if exec_result == None:
        connection.commit()
        cursor.close()
        connection.close()
        return {
            "msg": "Data Deleted Successfully (!if Existed)"
        }
    else:
        status_code.status_code = status.HTTP_202_ACCEPTED
        return {
            "Msg":" Could not delete post"
            }



    
@app.put("/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int):
    post_json = post.model_dump()
    #Create database connection
    connection = connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),database=os.getenv('DB_NAME'),password="redhat123")
    #Check if connection
    if not connection:
        sys.exit("Database not initialized. Exited...!!!")
    #create cursor
    cursor = connection.cursor()
    #Create query

    #TODO: Check if the post is existing first, and if it does then only update it 
    query = f'UPDATE {os.getenv("DB_TABLE_NAME")} SET title="{post_json["title"]}",age={post_json["age"]},firstname="{post_json["firstname"]}",lastname="{post_json["lastname"]}",content="{post_json["content"]}" where id={passed_id}'
    print(query)
    exec_result = cursor.execute(query)
    if exec_result == None:
        connection.commit()
        cursor.close()
        connection.close()
        return {
            "msg": "Data Updated Successfully"
        }
    else:
        status_code = status.HTTP_202_ACCEPTED
        return {
            "Msg":" Could not update post"
            }

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
