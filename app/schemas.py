from pydantic import BaseModel,EmailStr

class post_schema(BaseModel):
    title: str
    firstname: str
    lastname: str
    content: str

class post_response(post_schema):
    class Config:
        from_attributes = True

class user_create(BaseModel):
    email: EmailStr
    password: str

class user_create_respones(BaseModel):
    email: EmailStr
    class Config:
        from_attributes = True

    