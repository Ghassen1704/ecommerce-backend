# models/__init__.py
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()  # Base object that all models will inherit from
from .user import User
from .product import Product
from .pricing import Pricing