from datetime import datetime, timedelta
from jose import jwt
from database import find_user_in_db
from os import getenv
from dotenv import load_dotenv

load_dotenv()
#This code returns a JWT token upon user login.
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    payload_encode = payload.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #create token expiry time ( token is valid for 30m from now )
    payload_encode.update({"exp": expire_time})

    #generate JWT token
    return jwt.encode(payload_encode,SECRET_KEY,algorithm=ALGORITHM)

def validate_access_token(token: str):
    try:
        extract_jwt_from_header = token.split()[1]
        payload = jwt.decode(extract_jwt_from_header,SECRET_KEY,ALGORITHM)
        user_email_in_jwt = payload.get('email')
        user_email_in_database = find_user_in_db(user_email_in_jwt)[0]
        token_expire = payload.get("exp")
        if user_email_in_jwt is not None:
            return {"email": user_email_in_jwt,"expire": False,"msg":f'Welcome {user_email_in_jwt}'} if user_email_in_jwt == user_email_in_database else {"email": user_email_in_jwt,"expire": False,"msg":f'Invalid User Email {user_email_in_jwt}'}
                
        
    except:
        return {"expire": True,"msg": "Token Expired. Please Login Again."}
        
    