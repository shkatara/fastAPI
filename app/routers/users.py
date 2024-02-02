from schemas import user_create, user_create_respones
from database import conn,posts_table,users_table
from fastapi import Response,status,APIRouter
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
def userCreate(userdata: user_create,status_code: Response):
    find_user = users_table.select().where(users_table.c.email == userdata.email)
    exec_sql = conn.execute(find_user).fetchone()
    if exec_sql != None:
        status_code.status_code = status.HTTP_208_ALREADY_REPORTED
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
def userLogin(userdata: user_create,status_code: Response):
    find_user = users_table.select().where(users_table.c.email == userdata.email)
    exec_sql = conn.execute(find_user).fetchone()
    if exec_sql == None:
        status_code.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Username or password incorrect"}
    encoded_hash = exec_sql[1].encode('utf-8')
    calc_hash = hashpw(userdata.password.encode('utf-8'),exec_sql[2].encode('utf-8'))
    return {"msg": "User Logged in successfully"} if encoded_hash == calc_hash else {"msg": "User login Failed"}
    
