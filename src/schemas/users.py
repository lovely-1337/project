from pydantic import BaseModel, EmailStr


class UserRequestADD(BaseModel):
    email: EmailStr
    password: str

class UserADD(BaseModel):
    email: EmailStr
    hashed_password: str



class User(BaseModel):
    id : int
    email: EmailStr



class UserWithHashedPassword(User):
    hashed_password: str
   