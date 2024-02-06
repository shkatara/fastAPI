from database import conn,posts_table,Select,find_post_in_db
from fastapi import Request,Response,status,APIRouter,Header
from oauth2 import validate_access_token
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack

from schemas import post_schema

posts_router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]

)

@posts_router.get("/list")
def list_posts(Authorization: str = Header(default=None)):
    token = Authorization
    if validate_access_token(token)['expire']:
        return {"Error": "Token Invalid."}
    else:
        result_list = []
        select_sql_instruction = Select(posts_table.c.title,posts_table.c.content, posts_table.c.firstname, posts_table.c.lastname)
        exec_sql = conn.execute(select_sql_instruction).all()
        for row in exec_sql: 
            result_list = result_list + [list(row)]
        return result_list
    

@posts_router.get("/fetch/{passed_id}", status_code=status.HTTP_200_OK)
async def post_by_id(passed_id: int, status_code: Response,Authorization: str = Header(default=None)):
    token = Authorization
    if validate_access_token(token)['expire']:
        return {"Error": "Token Invalid."}
    else:
        post = find_post_in_db(passed_id)
        return post

    
@posts_router.post("/create",status_code=status.HTTP_201_CREATED)
def create_item(post: post_schema, Authorization: str = Header(default=None)):
    token = Authorization
    if validate_access_token(token)['expire']:
        return {"Error": "Token Invalid."}
    else:
        insert_sql_statement = posts_table.insert().values(title=post.title,firstname=post.firstname,lastname=post.lastname,content=post.content)
        conn.execute(insert_sql_statement)
        return {"msg": "Data inserted successfully"} if conn.commit() is None else {"msg": "Data not inserted successfully"}


@posts_router.delete("/delete/{passed_id}")
def delete_post(passed_id: int,status_code: Response,Authorization: str = Header(default=None)):
    token = Authorization
    if validate_access_token(token)['expire']:
        return {"Error": "Token Invalid."}
    else:
        findPost = find_post_in_db(passed_id)
        if isinstance(findPost,dict):
            return {"msg":"Post Not Found"}
        delete_sql_instruction = posts_table.delete().where(posts_table.c.id == passed_id)
        conn.execute(delete_sql_instruction)
        return {"msg": "Post Succesfully deleted"} if conn.commit() is None else {"msg": "Post Not deleted"}
    
@posts_router.put("/update/{passed_id}",status_code=status.HTTP_200_OK)
def update(post: post_schema, passed_id: int,Authorization: str = Header(default=None)):
    token = Authorization
    if validate_access_token(token)['expire']:
        return {"Error": "Token Invalid."}
    else:
        findPost = find_post_in_db(passed_id)
        if isinstance(findPost,dict):
            return {"msg":"Post Not Found"}
        update_post_sql = posts_table.update().where(posts_table.c.id == passed_id).values(title=post.title,firstname=post.firstname,lastname=post.lastname,content=post.content)
        conn.execute(update_post_sql)
        return {"msg": "Post Succesfully Updated"} if conn.commit() is None else {"msg": "Post Not updated"}