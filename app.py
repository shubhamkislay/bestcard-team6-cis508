import streamlit as st
import pickle
import numpy as np

# -------------------------------
# Custom CSS for Modern Look with White Heading
# -------------------------------
st.markdown("""
    <style>
    /* Page background */
    .reportview-container {
        background: #F0F2F6;
    }
    /* Header styles with white heading */
    .big-font {
        font-size: 50px !important;
        color: white !important;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-font {
        font-size: 20px !important;
        color: #666666;
        text-align: center;
        margin-top: 0;
        margin-bottom: 20px;
    }
    /* Button style */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    /* Input field styling */
    .stNumberInput>div>div>input {
        font-size: 16px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Header Section
# -------------------------------
st.markdown('<p class="big-font">Team 6 BestCard Demo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Predicting Credit Default Risk</p>', unsafe_allow_html=True)

# -------------------------------
# Load the Pre-trained Model
# -------------------------------
with open('xgb_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

# -------------------------------
# Helper Functions
# -------------------------------
def load_sample_data(sample_type):
    if sample_type == "defaulter":
        st.session_state["limit_bal"] = 50000.0
        st.session_state["sex"] = 1
        st.session_state["education_numeric"] = 2
        st.session_state["education_level"] = "High School"
        st.session_state["marriage"] = 1
        st.session_state["age"] = 40
        
        # Payment history indicating late payments
        st.session_state["pay_1"] = 4
        st.session_state["pay_2"] = 3
        st.session_state["pay_3"] = 2
        st.session_state["pay_4"] = 1
        st.session_state["pay_5"] = 0
        st.session_state["pay_6"] = 0
        
        # Higher billing amounts and very low payments
        st.session_state["bill_amt1"] = 5000.0
        st.session_state["bill_amt2"] = 5200.0
        st.session_state["bill_amt3"] = 5400.0
        st.session_state["bill_amt4"] = 5600.0
        st.session_state["bill_amt5"] = 5800.0
        st.session_state["bill_amt6"] = 6000.0
        
        st.session_state["pay_amt1"] = 200.0
        st.session_state["pay_amt2"] = 200.0
        st.session_state["pay_amt3"] = 200.0
        st.session_state["pay_amt4"] = 200.0
        st.session_state["pay_amt5"] = 200.0
        st.session_state["pay_amt6"] = 200.0
    elif sample_type == "non_defaulter":
        # Values indicating healthy repayment behavior
        st.session_state["limit_bal"] = 100000.0
        st.session_state["sex"] = 1
        st.session_state["education_numeric"] = 1
        st.session_state["education_level"] = "Graduate School"
        st.session_state["marriage"] = 1
        st.session_state["age"] = 35
        
        # Payment history with minimal delays
        st.session_state["pay_1"] = 0
        st.session_state["pay_2"] = 2
        st.session_state["pay_3"] = 0
        st.session_state["pay_4"] = 0
        st.session_state["pay_5"] = 0
        st.session_state["pay_6"] = 0
        
        # Lower billing amounts (indicating low credit usage)
        st.session_state["bill_amt1"] = 120.0
        st.session_state["bill_amt2"] = 0.0
        st.session_state["bill_amt3"] = 0.0
        st.session_state["bill_amt4"] = 0.0
        st.session_state["bill_amt5"] = 0.0
        st.session_state["bill_amt6"] = 0.0
        
        # Healthy payments (sufficient to cover bills)
        st.session_state["pay_amt1"] = 120.0
        st.session_state["pay_amt2"] = 0.0
        st.session_state["pay_amt3"] = 0.0
        st.session_state["pay_amt4"] = 0.0
        st.session_state["pay_amt5"] = 0.0
        st.session_state["pay_amt6"] = 0.0

def clear_fields():
    st.session_state["limit_bal"] = 10000.0
    st.session_state["sex"] = 1
    st.session_state["education_numeric"] = 2
    st.session_state["education_level"] = "Graduate School"
    st.session_state["marriage"] = 1
    st.session_state["age"] = 30
    st.session_state["pay_1"] = 0
    st.session_state["pay_2"] = 0
    st.session_state["pay_3"] = 0
    st.session_state["pay_4"] = 0
    st.session_state["pay_5"] = 0
    st.session_state["pay_6"] = 0
    st.session_state["bill_amt1"] = 0.0
    st.session_state["bill_amt2"] = 0.0
    st.session_state["bill_amt3"] = 0.0
    st.session_state["bill_amt4"] = 0.0
    st.session_state["bill_amt5"] = 0.0
    st.session_state["bill_amt6"] = 0.0
    st.session_state["pay_amt1"] = 0.0
    st.session_state["pay_amt2"] = 0.0
    st.session_state["pay_amt3"] = 0.0
    st.session_state["pay_amt4"] = 0.0
    st.session_state["pay_amt5"] = 0.0
    st.session_state["pay_amt6"] = 0.0

# -------------------------------
# Initialize Default Session State Values
# -------------------------------
default_keys = {
    "limit_bal": 10000.0,
    "sex": 1,
    "education_numeric": 2,
    "education_level": "Graduate School",
    "marriage": 1,
    "age": 30,
    "pay_1": 0,
    "pay_2": 0,
    "pay_3": 0,
    "pay_4": 0,
    "pay_5": 0,
    "pay_6": 0,
    "bill_amt1": 0.0,
    "bill_amt2": 0.0,
    "bill_amt3": 0.0,
    "bill_amt4": 0.0,
    "bill_amt5": 0.0,
    "bill_amt6": 0.0,
    "pay_amt1": 0.0,
    "pay_amt2": 0.0,
    "pay_amt3": 0.0,
    "pay_amt4": 0.0,
    "pay_amt5": 0.0,
    "pay_amt6": 0.0
}
for key, default_value in default_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# -------------------------------
# Sample Buttons
# -------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Sample Defaulter"):
        load_sample_data("defaulter")
with col2:
    if st.button("Sample Non-Defaulter"):
        load_sample_data("non_defaulter")
with col3:
    if st.button("Clear"):
        clear_fields()

# -------------------------------
# Input Fields
# -------------------------------
limit_bal = st.number_input("Credit Limit (LIMIT_BAL)", min_value=0.0, key="limit_bal")
sex = st.selectbox("Sex", options=[1, 2], key="sex")
education_numeric = st.number_input("Education (Numeric)", min_value=1, key="education_numeric")
education_level = st.selectbox("Education Level", 
    options=["Graduate School", "High School", "None", "Others", "University"], key="education_level")
marriage = st.selectbox("Marriage", options=[1, 2, 3], key="marriage")
age = st.number_input("Age", min_value=18, key="age")

pay_1 = st.number_input("PAY_1", min_value=-2, max_value=8, key="pay_1")
pay_2 = st.number_input("PAY_2", min_value=-2, max_value=8, key="pay_2")
pay_3 = st.number_input("PAY_3", min_value=-2, max_value=8, key="pay_3")
pay_4 = st.number_input("PAY_4", min_value=-2, max_value=8, key="pay_4")
pay_5 = st.number_input("PAY_5", min_value=-2, max_value=8, key="pay_5")
pay_6 = st.number_input("PAY_6", min_value=-2, max_value=8, key="pay_6")

bill_amt1 = st.number_input("BILL_AMT1", key="bill_amt1")
bill_amt2 = st.number_input("BILL_AMT2", key="bill_amt2")
bill_amt3 = st.number_input("BILL_AMT3", key="bill_amt3")
bill_amt4 = st.number_input("BILL_AMT4", key="bill_amt4")
bill_amt5 = st.number_input("BILL_AMT5", key="bill_amt5")
bill_amt6 = st.number_input("BILL_AMT6", key="bill_amt6")

pay_amt1 = st.number_input("PAY_AMT1", key="pay_amt1")
pay_amt2 = st.number_input("PAY_AMT2", key="pay_amt2")
pay_amt3 = st.number_input("PAY_AMT3", key="pay_amt3")
pay_amt4 = st.number_input("PAY_AMT4", key="pay_amt4")
pay_amt5 = st.number_input("PAY_AMT5", key="pay_amt5")
pay_amt6 = st.number_input("PAY_AMT6", key="pay_amt6")

# -------------------------------
# Derived Features Calculation
# -------------------------------
if st.session_state["limit_bal"] == 0:
    st.error("Credit Limit must be greater than 0.")
    st.stop()

credit_utilization = st.session_state["bill_amt6"] / st.session_state["limit_bal"]
repayment_ratio = (
    st.session_state["pay_amt1"] 
    + st.session_state["pay_amt2"] 
    + st.session_state["pay_amt3"] 
    + st.session_state["pay_amt4"] 
    + st.session_state["pay_amt5"] 
    + st.session_state["pay_amt6"]
) / st.session_state["limit_bal"]
payment_behavior_trend = st.session_state["pay_1"] - st.session_state["pay_6"]

# Education dummy variables
edu_dummy = {"Graduate School": 0, "High School": 0, "None": 0, "Others": 0, "University": 0}
edu_dummy[st.session_state["education_level"]] = 1

# -------------------------------
# Construct Input Vector
# -------------------------------
input_features = [
    st.session_state["limit_bal"],
    st.session_state["sex"],
    st.session_state["education_numeric"],
    st.session_state["marriage"],
    st.session_state["age"],
    st.session_state["pay_1"],
    st.session_state["pay_2"],
    st.session_state["pay_3"],
    st.session_state["pay_4"],
    st.session_state["pay_5"],
    st.session_state["pay_6"],
    st.session_state["bill_amt1"],
    st.session_state["bill_amt2"],
    st.session_state["bill_amt3"],
    st.session_state["bill_amt4"],
    st.session_state["bill_amt5"],
    st.session_state["bill_amt6"],
    st.session_state["pay_amt1"],
    st.session_state["pay_amt2"],
    st.session_state["pay_amt3"],
    st.session_state["pay_amt4"],
    st.session_state["pay_amt5"],
    st.session_state["pay_amt6"],
    edu_dummy["Graduate School"],
    edu_dummy["High School"],
    edu_dummy["None"],
    edu_dummy["Others"],
    edu_dummy["University"],
    credit_utilization,
    repayment_ratio,
    payment_behavior_trend
]

# -------------------------------
# Prediction Button
# -------------------------------
if st.button("Predict Default"):
    input_data = np.array(input_features).reshape(1, -1)
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1] if hasattr(model, "predict_proba") else None
    
    if prediction[0] == 1:
        st.error("Prediction: Customer is likely to default.")
    else:
        st.success("Prediction: Customer is unlikely to default.")
    
    if probability is not None:
        st.write(f"Default Probability: {probability:.2f}")
