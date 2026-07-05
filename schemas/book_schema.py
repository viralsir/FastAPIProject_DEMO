from pydantic import BaseModel, Field, ConfigDict


class AuthorResponse(BaseModel):
    id:int | None  = Field(...,description="author id")
    name:str | None = Field(...,description="author name")
    email:str | None = Field(...,description="author email")

    model_config = ConfigDict(from_attributes=True)

class BookResponse(BaseModel):
    id:int | None
    title :str | None
    author:int
    authorinfo:AuthorResponse | None
    price :int | None

    model_config = ConfigDict(from_attributes=True)

