# models/product.py
from sqlalchemy import Column, Integer, String, Float
from database import Base  # Import Base from database.py

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String(255))
    price = Column(Float)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
