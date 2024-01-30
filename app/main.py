from fastapi import FastAPI,Request,Response,status
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
import uvicorn
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Select
from schemas import post_schema , post_response

#Load environment values from .env file



app = FastAPI()

#create engine for sqlalchemy
engine = create_engine("mysql+pymysql://root:redhat123@localhost/posts")

#create connection to mysql
conn = engine.connect()

#meta object to hold table metadata
posts_table_meta = MetaData()

#define table structure
posts_table = Table('posts',posts_table_meta,Column('id', Integer, primary_key=True, autoincrement=True),Column('title', String(255)),Column('firstname', String(255)),Column('lastname', String(255)),Column('content',String(255)))
posts_table_meta.create_all(engine)


def find_post_in_db(post_id):
    select_sql_where_instruction = Select(posts_table.c.title,posts_table.c.content, posts_table.c.firstname, posts_table.c.lastname).where(posts_table.c.id == post_id)
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
    select_sql_instruction = Select(posts_table.c.title,posts_table.c.content, posts_table.c.firstname, posts_table.c.lastname)
    exec_sql = conn.execute(select_sql_instruction).all()
    for row in exec_sql: 
        print(row)
        result_list = result_list + [{"title":row[0]},{"content":row[1]},{"firstname":row[2]},{"lastname":row[3]}]
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
    return {"msg": "Data inserted successfully"} if commit == None else {"msg": "Data not inserted successfully"}
    

@app.delete("/delete/post/{passed_id}")
def delete_post(passed_id: int,status_code: Response):
    select_sql_instruction = posts_table.select().where(posts_table.c.id == passed_id)
    exec_sql = conn.execute(select_sql_instruction).fetchone()
    if exec_sql == None:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Post not found"}
    delete_sql_instruction = posts_table.delete().where(posts_table.c.id == passed_id)
    conn.execute(delete_sql_instruction)
    delete_commit = conn.commit()
    return {"msg": "Post Succesfully deleted"} if delete_commit == None else {"msg": "Post Not deleted"}
   

    
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
    post =  find_post_in_db(passed_id)
    return post
    #not working yet. Need to see how to pass only the user provided keys in database, without hardcoding them.






#start main app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
