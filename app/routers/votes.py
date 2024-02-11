from schemas import user_create,user_token_validate
from sqlalchemy import Column, String,Integer,Table,MetaData,create_engine,Select,ForeignKey
from database import conn,posts_table,Select,find_post_in_db,users_table
from oauth2 import create_access_token,validate_access_token
from fastapi import Response,status,APIRouter,Header
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
from bcrypt import gensalt, hashpw

votes_router = APIRouter(
    prefix="/votes",
    tags = ["Votes"]
)

@votes_router.get("/list")
def data():
    return {"votes": "Hello"}

@votes_router.post("/vote_post/")
def data(Authorization: str = Header(default=None), response:str = Response):
    token = Authorization
    if validate_access_token(token)['expire']:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Error": "Token Expired."}
    else:
        select_sql_instruction = Select(posts_table.c.post_title,posts_table.c.post_content).where(posts_table.c.post_owner==validate_access_token(token)['email']).join(users_table)
        exec_sql = conn.execute(select_sql_instruction).fetchall()
        return [dict(data._mapping) for data in exec_sql] #convert all the returned data to dict
    