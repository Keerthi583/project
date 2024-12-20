from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Load the trained Random Forest model
try:
    model = joblib.load("final_random_forest_model.joblib")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading the model: {e}")
    raise e

# Define input schema using Pydantic
class LoanApplication(BaseModel):
    person_age: int
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    credit_score: float
    previous_loan_defaults_on_file: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Loan Status Prediction API. Use /predict to get predictions."}

# Prediction endpoint
@app.post("/predict/")
def predict(application: LoanApplication):
    try:
        # Convert the input data to a DataFrame
        input_data = pd.DataFrame([{
            "person_age": application.person_age,
            "person_gender": application.person_gender,
            "person_education": application.person_education,
            "person_income": application.person_income,
            "person_emp_exp": application.person_emp_exp,
            "person_home_ownership": application.person_home_ownership,
            "loan_amnt": application.loan_amnt,
            "loan_intent": application.loan_intent,
            "loan_int_rate": application.loan_int_rate,
            "loan_percent_income": application.loan_percent_income,
            "cb_person_cred_hist_length": application.cb_person_cred_hist_length,
            "credit_score": application.credit_score,
            "previous_loan_defaults_on_file": application.previous_loan_defaults_on_file
        }])

        # Get predictions from the model
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)[:, 1]  # Probability for the positive class

        # Interpret the prediction
        loan_status = "Approved" if prediction[0] == 1 else "Rejected"

        return {
            "loan_status": loan_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
