from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass
 
class PostResponse(PostBase):
    id:int
    created_at : datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str

    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None
