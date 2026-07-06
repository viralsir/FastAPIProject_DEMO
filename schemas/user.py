from pydantic import BaseModel, EmailStr,Field


class RegisterRequest(BaseModel):
    id:int = Field(...)
    email:str
    hash_password:str = Field(...,max_length=8)
    role:str

class LoginRequest(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    role:str

