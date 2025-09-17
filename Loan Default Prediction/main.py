from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from typing import Optional

# 1️⃣ Load saved pipeline
pipeline = joblib.load("models/loan_default_pipeline.pkl")

# 2️⃣ Initialize FastAPI
app = FastAPI(title="Loan Default Prediction API")

class PredictionResponse(BaseModel):
    prediction: int
    probability_of_default: float
    risk: str

# 3️⃣ Define input schema
class LoanApplication(BaseModel):
    LoanID: Optional[str] = Field(default=None, title="LoanID")
    Age: float
    Income: float
    LoanAmount: float
    CreditScore: float
    MonthsEmployed: float
    NumCreditLines: float
    InterestRate: float
    LoanTerm: float
    DTIRatio: float
    Education: str
    EmploymentType: str
    MaritalStatus: str
    HasMortgage: str
    HasDependents: str
    LoanPurpose: str
    HasCoSigner: str

# 4️⃣ Health check route
@app.get("/")
def read_root():
    return {"message": "Loan Default Prediction API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 5️⃣ Prediction route
@app.post("/predict")
def predict_default(application: LoanApplication):
    # Convert request to DataFrame
    data = pd.DataFrame([application.dict()])

    # Make prediction
    pred = pipeline.predict(data)[0]
    pred_proba = pipeline.predict_proba(data)[0][1]

    # Return results
    return {
        "LoanID": application.LoanID,
        "prediction": int(pred),  # 0 = No Default, 1 = Default
        "probability_of_default": round(float(pred_proba), 4),
        "risk": "High" if pred_proba > 0.7 else "Medium" if pred_proba > 0.4 else "Low"
    }
