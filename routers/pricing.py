# routers/pricing.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Pricing
from database import SessionLocal  # Assuming you have a session setup in a separate file
import random

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get pricing for a specific product
@router.get("/pricing/{product_id}")
def get_pricing(product_id: int, db: Session = Depends(get_db)):
    pricing = db.query(Pricing).filter(Pricing.product_id == product_id).first()
    if pricing is None:
        raise HTTPException(status_code=404, detail="Pricing not found")
    return pricing

# Update pricing for a specific product
@router.put("/pricing/{product_id}")
def update_pricing(product_id: int, base_price: float, discount: float, db: Session = Depends(get_db)):
    pricing = db.query(Pricing).filter(Pricing.product_id == product_id).first()
    if pricing is None:
        raise HTTPException(status_code=404, detail="Pricing not found")
    
    pricing.base_price = base_price
    pricing.discount = discount
    pricing.calculate_final_price()  # Recalculate the final price based on new values
    db.commit()
    return pricing
@router.post("/generate_fake_data/")
def generate_fake_data(num_records: int = 100, db: Session = Depends(get_db)):
    for _ in range(num_records):
        product_id = random.randint(1000, 9999)
        base_price = round(random.uniform(50.0, 500.0), 2)
        discount = round(random.uniform(5.0, 50.0), 2)
        final_price = round(base_price - (base_price * discount / 100), 2)

        pricing = Pricing(
            product_id=product_id,
            base_price=base_price,
            discount=discount,
            final_price=final_price
        )

        db.add(pricing)
    db.commit()
    return {"message": f"{num_records} fake records created!"}