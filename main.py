from fastapi import FastAPI,Depends
from models import user
from models import pricing 
from models import product
from routers import products, users
from routers import pricing,graphql_api,ai_pricing,sales_forecasting
from routers.auth import router as auth_router 
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
from faker import Faker
from sqlalchemy.orm import Session
import random
fake = Faker()

app = FastAPI(title="E-Commerce API", version="1.0")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods like GET, POST
    allow_headers=["*"],  # Allow all headers, including custom headers
)
# Include routers (microservices)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])
app.include_router(graphql_api.router, tags=["GraphQL"])
app.include_router(ai_pricing.router, tags=["AIPricing"])
app.include_router(sales_forecasting.router, tags=["Forecasting"])
app.include_router(auth_router, tags=["Auth"])

@app.post("/generate_fake_data/")
def generate_fake_data(num_users: int = 100, num_products: int = 100, db: Session = Depends(get_db)):
    # Generate fake users
    for _ in range(num_users):
        name = fake.name()
        email = fake.email()
        password = fake.password()  # Use a random password for testing

        fake_user = user.User(
            username=name,
            email=email,
            hashed_password=password
        )
        db.add(fake_user)

    # Generate fake products and pricing
    for _ in range(num_products):
        name = fake.word().capitalize()  # Random product name
        description = fake.sentence()  # Random product description
        price = round(random.uniform(10.0, 1000.0), 2)  # Random price between 10 and 1000

        fake_product = product.Product(
            name=name,
            description=description,
            price=price,
        )
        db.add(fake_product)

        # Generate fake pricing for the product
        base_price = price
        discount = round(random.uniform(5.0, 50.0), 2)  # Random discount between 5% and 50%
        final_price = round(base_price - (base_price * discount / 100), 2)

        fake_pricing = pricing.Pricing(
            product_id=fake_product.id,  # Associate the pricing with the generated product
            base_price=base_price,
            discount=discount,
            final_price=final_price
        )
        db.add(fake_pricing)

    db.commit()  # Commit all the changes to the database

    return {"message": f"{num_users} fake users, {num_products} fake products, and pricing data created!"}

@app.get("/")
def home():
    return {"message": "Welcome to the E-Commerce API!"}
