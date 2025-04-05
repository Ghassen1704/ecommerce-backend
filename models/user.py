# models/user.py
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # Relationship example: If users can have products
    # products = relationship("Product", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
