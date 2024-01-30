from pydantic import BaseModel

class post_schema(BaseModel):
    title: str
    firstname: str
    lastname: str
    content: str

class post_response(post_schema):
    class Config:
        from_attributes = True