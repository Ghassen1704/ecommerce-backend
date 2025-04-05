import pandas as pd
import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import xgboost as xgb
from datetime import datetime
from io import StringIO
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .dependencies import get_current_user

router = APIRouter()
class SalesPredictionRequest(BaseModel):
    past_sales: list

# Prediction function for 7-day forecast
def predict_sales(sales_data):
    # Preprocess the data
    sales_data['date'] = pd.to_datetime(sales_data['date'])
    sales_data['day_of_week'] = sales_data['date'].dt.dayofweek
    sales_data['rolling_mean'] = sales_data['sales'].rolling(window=3).mean().shift(1)
    
    # Prepare the data for XGBoost (features + target)
    X = sales_data[['day_of_week', 'rolling_mean']].fillna(0)  # Filling NaN values
    y = sales_data['sales']
    
    # Train the model (this is a simplified approach)
    model = xgb.XGBRegressor()
    model.fit(X, y)
    
    # Predict the next 7 days (using last day's data and forecasting future)
    last_data = X.iloc[-1:].values
    predicted_sales = []
    
    for i in range(7):
        prediction = model.predict(last_data)
        predicted_sales.append(float(prediction[0]))  # Convert numpy.float32 to native float
        
        # Update the features for the next prediction
        last_data[0, 0] = (last_data[0, 0] + 1) % 7  # Move to the next day of the week (0-6)
        last_data[0, 1] = prediction[0]  # Update rolling mean with the predicted value
        
        # Update rolling mean: Calculate the new rolling mean based on the new prediction
        rolling_window = np.append(sales_data['sales'].values[-2:], prediction[0])  # Last 2 actual sales + new prediction
        last_data[0, 1] = np.mean(rolling_window)
    
    return predicted_sales
@router.post("/predict_sales/")
async def predict_sales_route(file: UploadFile = File(...)):
    """
    Handles the upload of a CSV file, validates it, and makes sales predictions for the next 7 days.
    """
    try:
        # Read the uploaded CSV file content
        content = await file.read()

        # Read the CSV content into a pandas DataFrame
        sales_data = pd.read_csv(StringIO(content.decode('utf-8')))
        
        # Check if 'date' and 'sales' columns exist in the data
        if 'date' not in sales_data.columns or 'sales' not in sales_data.columns:
            raise ValueError("CSV must contain 'date' and 'sales' columns.")
        
        # Convert the 'date' column to datetime format (if necessary)
        sales_data['date'] = pd.to_datetime(sales_data['date'], errors='coerce')

        # Drop rows with invalid date values
        sales_data = sales_data.dropna(subset=['date'])

        # Predict sales for the next 7 days using the prediction function
        predicted_sales = predict_sales(sales_data)
        
        # Return the predicted sales
        return {"predicted_sales": predicted_sales}
    
    except Exception as e:
        # Return any error encountered during processing
        return {"error": str(e)}