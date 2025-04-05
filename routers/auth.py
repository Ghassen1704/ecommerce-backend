from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from schemas.user import UserBase  # Import Pydantic schemas
from database import SessionLocal
from passlib.context import CryptContext
from .jwt_utils import create_access_token, decode_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Register user
@router.post("/register/")
def register(user: UserBase, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and create a new user
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# Pydantic model for returning JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# Login endpoint
@router.post("/login/", response_model=Token)
def login(user: UserBase, db: Session = Depends(get_db)):
    # Fetch user from the database
    db_user = db.query(User).filter(User.username == user.username).first()

    # Verify if the user exists and the password matches
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create an access token for the user
    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}
