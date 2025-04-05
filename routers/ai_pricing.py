import xgboost as xgb
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .dependencies import get_current_user


router = APIRouter()
# Define the Pydantic model for input validation
class PricePredictionRequest(BaseModel):
    demand: int
    season: int
# Load sample sales data
data = pd.DataFrame({
    "demand": np.random.randint(10, 500, 100),
    "price": np.random.uniform(20, 200, 100),
    "season": np.random.randint(0, 4, 100),
})

# Train Model
X = data[["demand", "season"]]
y = data["price"]
model = xgb.XGBRegressor()
model.fit(X, y)


# Prediction function
def predict_price(demand: int, season: int):
    return model.predict(np.array([[demand, season]]))[0]

# Define the POST route for predicting price
@router.post("/predict_price/")
def predict_price_route(request: PricePredictionRequest):
    try:
        # Call the prediction function and cast the result to a float
        predicted_price = float(predict_price(request.demand, request.season))
        return {"predicted_price": round(predicted_price, 2)}
    except Exception as e:
        # Return a 400 error if prediction fails
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")