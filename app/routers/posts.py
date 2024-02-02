from database import conn,posts_table,Select,find_post_in_db
from fastapi import Request,Response,status,APIRouter
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack

from schemas import post_schema

posts_router = APIRouter()

@posts_router.get("/")
async def users():
    return {
        "Hello": "World"
    }

@posts_router.get("/posts/list")
def users():
    result_list = []
    select_sql_instruction = Select(posts_table.c.title,posts_table.c.content, posts_table.c.firstname, posts_table.c.lastname)
    exec_sql = conn.execute(select_sql_instruction).all()
    for row in exec_sql: 
        result_list = result_list + [list(row)]
    return result_list

@posts_router.get("/posts/fetch/{passed_id}", status_code=status.HTTP_200_OK)
async def post_by_id(passed_id: int, status_code: Response):
    post = find_post_in_db(passed_id)
    return post
  
    
@posts_router.post("/posts/create",status_code=status.HTTP_201_CREATED)
def create_item(post: post_schema):
    post_json = post.model_dump()
    insert_sql_statement = posts_table.insert().values(title=post_json['title'],firstname=post_json['firstname'],lastname=post_json['lastname'],content=post_json['content'])
    conn.execute(insert_sql_statement)
    commit = conn.commit()
    return {"msg": "Data inserted successfully"} if commit == None else {"msg": "Data not inserted successfully"}
    

@posts_router.delete("/posts/delete{passed_id}")
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
   

    
@posts_router.put("/posts/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int):
    post_json = post.model_dump()
    post = find_post_in_db(passed_id)
    update_post_sql = posts_table.update().where(posts_table.c.id == passed_id).values(title=post_json['title'],firstname=post_json['firstname'],lastname=post_json['lastname'],content=post_json['content'])
    conn.execute(update_post_sql)
    update_commit = conn.commit()
    print(update_commit)

