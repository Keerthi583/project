import streamlit as st
import requests

# Backend URL
backend_url = "https://project-1-k64w.onrender.com/predict/"

# Streamlit UI
st.title("Loan Status Prediction")
st.write("Enter the details to predict loan status:")

# Input Fields
person_age = st.number_input("Person's Age:", min_value=18, max_value=100, value=30)
person_gender = st.selectbox("Person's Gender:", ["male", "female"])
person_education = st.selectbox("Education Level:", ["high_school", "bachelors", "masters", "phd"])
person_income = st.number_input("Annual Income:", min_value=0, value=50000)
person_emp_exp = st.number_input("Years of Employment Experience:", min_value=0, value=5)
person_home_ownership = st.selectbox("Home Ownership:", ["rent", "own", "mortgage", "other"])
loan_amnt = st.number_input("Loan Amount:", min_value=0, value=10000)
loan_intent = st.selectbox("Loan Intent:", ["education", "medical", "personal", "venture", "home", "other"])
loan_int_rate = st.number_input("Loan Interest Rate (%):", min_value=0.0, value=7.5)
loan_percent_income = st.number_input("Loan Amount as % of Income:", min_value=0.0, value=0.2)
cb_person_cred_hist_length = st.number_input("Credit History Length (Years):", min_value=0, value=10)
credit_score = st.number_input("Credit Score:", min_value=300, max_value=850, value=650)
previous_loan_defaults_on_file = st.selectbox("Previous Loan Defaults on File:", ["No", "Yes"])

# Submit Button
if st.button("Predict Loan Status"):
    # Prepare input data
    input_data = {
        "person_age": person_age,
        "person_gender": person_gender,
        "person_education": person_education,
        "person_income": person_income,
        "person_emp_exp": person_emp_exp,
        "person_home_ownership": person_home_ownership,
        "loan_amnt": loan_amnt,
        "loan_intent": loan_intent,
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": cb_person_cred_hist_length,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": previous_loan_defaults_on_file,
    }

    # Make POST request to FastAPI backend
    try:
        response = requests.post(backend_url, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            # Display results
            st.success(f"Loan Status: {prediction.get('loan_status', 'Unknown')}")
            reason = prediction.get("reason")
            if reason:
                st.write(f"Reason: {reason}")
        else:
            st.error(f"Error: {response.status_code}, {response.json()}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
