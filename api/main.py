from fastapi import FastAPI
from pydantic import BaseModel, Field

from E_Commerce_Customer_Segmentation.pipeline.stage_06_prediction import PredictionPipeline



# Create FastAPI application
app = FastAPI(
    title="E-Commerce Customer Segmentation API",
    description="API for predicting customer segments using GMM",
    version="1.0.0"
)


# Request data structure
class CustomerData(BaseModel):

    recency: float = Field(ge=0)
    frequency: float = Field(gt=0)
    monetary: float = Field(gt=0)


# Create prediction pipeline
prediction_pipeline = PredictionPipeline()


# Home endpoint
@app.get("/")
def home():

    return {
        "message": "E-Commerce Customer Segmentation API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict_customer(customer: CustomerData):

    result = prediction_pipeline.main(
        recency=customer.recency,
        frequency=customer.frequency,
        monetary=customer.monetary
    )

    return {
        "cluster": result["Cluster"],
        "membership_probability": result["Membership_Probability"]
    }