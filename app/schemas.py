from pydantic import BaseModel

class post_schema(BaseModel):
    title: str
    firstname: str
    lastname: str
    content: str