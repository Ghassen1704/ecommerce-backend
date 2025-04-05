from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be converted to Pydantic models
