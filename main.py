import joblib
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Load your trained pipeline
pipeline = joblib.load("loan_default_model.pkl")

# Define your input data model (adjust types as needed)
class LoanInput(BaseModel):
    LoanID: str
    Age: int
    Income: float
    LoanAmount: float
    CreditScore: int
    MonthsEmployed: int
    NumCreditLines: int
    InterestRate: float
    LoanTerm: int
    DTIRatio: float
    Education: str
    EmploymentType: str
    MaritalStatus: str
    HasMortgage: str
    HasDependents: str
    LoanPurpose: str
    HasCoSigner: str

# Label encodings (use the same as in training)
education_map = {"Graduate": 1, "HighSchool": 0}
employment_map = {"Salaried": 1, "SelfEmployed": 0}
marital_map = {"Married": 1, "Single": 0}
mortgage_map = {"Yes": 1, "No": 0}
dependents_map = {"Yes": 1, "No": 0}
purpose_map = {"Car": 0, "Home": 1, "Personal": 2}  # adjust as per your training
cosigner_map = {"Yes": 1, "No": 0}

def preprocess_input(data: LoanInput):
    return [
        data.Age,
        data.Income,
        data.LoanAmount,
        data.CreditScore,
        data.MonthsEmployed,
        data.NumCreditLines,
        data.InterestRate,
        data.LoanTerm,
        data.DTIRatio,
        education_map.get(data.Education, 0),
        employment_map.get(data.EmploymentType, 0),
        marital_map.get(data.MaritalStatus, 0),
        mortgage_map.get(data.HasMortgage, 0),
        dependents_map.get(data.HasDependents, 0),
        purpose_map.get(data.LoanPurpose, 0),
        cosigner_map.get(data.HasCoSigner, 0)
    ]

@app.post("/predict")
async def predict(input_data: LoanInput):
    X = [preprocess_input(input_data)]
    prediction = pipeline.predict(X)[0]
    return {"prediction": int(prediction)}

