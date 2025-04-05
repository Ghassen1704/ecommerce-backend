# schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str  # this should be the plain password

    class Config:
        orm_mode = True  # to allow conversion from ORM model to Pydantic model
