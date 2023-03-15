from pydantic import BaseModel
from typing import Optional


class structure(BaseModel):
    user_name: str
    email: str
    password: str
    contact: str
    address: str


class show_data(BaseModel):
    id : int
    user_name: str
    email: str
    contact: str
    address: str

    class Config():
        orm_mode = True


class login_details(BaseModel):
    email: str
    password: str
    otp : int

class show_secret_data(BaseModel):
    jwt: str
    otp: int
    created_date: str
    last_updated: str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]= None


