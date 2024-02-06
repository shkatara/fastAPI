from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi import Header

#This code returns a JWT token upon user login.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    payload_encode = payload.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #create token expiry time ( token is valid for 30m from now )
    payload_encode.update({"exp": expire_time})

    #generate JWT token
    return jwt.encode(payload_encode,SECRET_KEY,algorithm=ALGORITHM)

def return_token_info(header: str = Header(default=None)):
    return {"token": header}

def validate_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        user_email = payload.get('email')
        if user_email is not None:
            return {"email": user_email}   
    except:
        return {"msg":"Unauthenticated","detail":"Could not Validate Authentication. Please login again"}
    