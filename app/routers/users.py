from schemas import user_create,user_token_validate

from oauth2 import create_access_token,validate_access_token
from database import conn,users_table,find_user_in_db
from fastapi import Response,status,APIRouter,Header,Form
#Request from fastAPI contains the JSON data that can be used for retrieving what user had given. This is similar to fetching data from a HTTP_METHOD request in PHP that I worked on storastack
from bcrypt import gensalt, hashpw

users_router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

###################
#User registration#
###################
@users_router.post("/signup",status_code=status.HTTP_201_CREATED)
def userCreate(userdata: user_create,response: Response):
    findUser = find_user_in_db(userdata.email)
    if not isinstance(findUser,dict):
        response.status_code = status.HTTP_208_ALREADY_REPORTED
        return {"msg": "User already added"}
    password_bytes = userdata.password.encode('utf-8') 
    salt = gensalt()
    hash = hashpw(password_bytes,salt)
    sql = users_table.insert().values(email=userdata.email,password=hash,pass_salt=salt)
    conn.execute(sql)
    commit = conn.commit()
    return {"msg": "User added successfully"} if commit == None else {"msg": "User Not added"}

##################
#User login logic#
##################
@users_router.get("/login",status_code=status.HTTP_200_OK)
def userLogin(userdata: user_create,response: Response):
    findUser = find_user_in_db(userdata.email)
    if isinstance(findUser,dict):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Not Registered"}
    encoded_hash = findUser[1].encode('utf-8')
    calc_hash = hashpw(userdata.password.encode('utf-8'),findUser[2].encode('utf-8'))
    if encoded_hash != calc_hash:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": "Invalid Credentials"}
    else:
        token = create_access_token({'email':userdata.email})
    return {
        "token":token,
        "type": "Bearer"
    } 
    
@users_router.get("/lookup/self/",status_code=status.HTTP_200_OK,response_model=user_token_validate)
def userLookup(Authorization: str = Header(default=None)):
    token = Authorization
    return validate_access_token(token)