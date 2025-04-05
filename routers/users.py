# routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from database import get_db
from pydantic import BaseModel
from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Pydantic schema for creating a new user
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

# Pydantic schema for returning a user
class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True

# Hash password utility function
def hash_password(password: str):
    return pwd_context.hash(password)

# Create new user
@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)

    # Add the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Get user by ID
@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
