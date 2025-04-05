from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product
from schemas.product import ProductCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, category=product.category)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
