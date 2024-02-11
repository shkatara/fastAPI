from schemas import vote_schema
from database import conn,votes_table,find_post_in_db
from oauth2 import validate_access_token
from fastapi import Response,status,APIRouter,Header
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack


votes_router = APIRouter(
    prefix="/votes",
    tags = ["Votes"]
)

@votes_router.post("/vote_post/",status_code=status.HTTP_200_OK)
def data(response: Response,Authorization: str = Header(default=None), payload: dict = vote_schema):
    token = Authorization
    if validate_access_token(token)['expire']:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Error": "Token Expired."}
    else:
        post = find_post_in_db(payload['post_id'],validate_access_token(token)['email'])
        if isinstance(post,dict):
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"msg":"Post Not found"}
        sql = votes_table.insert().values(post_id=payload['post_id'],user_id=validate_access_token(token)['email'])
        print(sql)
        conn.execute(sql)
