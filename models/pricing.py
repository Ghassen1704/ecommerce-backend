# models/pricing.py

from sqlalchemy import Column, Integer, Float
from database import Base

class Pricing(Base):
    __tablename__ = "pricing"

    product_id = Column(Integer, primary_key=True, index=True)
    base_price = Column(Float)
    discount = Column(Float)
    final_price = Column(Float, nullable=True)

    # Method to calculate final price based on base price and discount
    def calculate_final_price(self):
        self.final_price = self.base_price - (self.base_price * self.discount / 100)
