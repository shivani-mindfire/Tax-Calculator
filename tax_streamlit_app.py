import streamlit as st
from services.TaxCalculator import TaxCalculator

st.set_page_config(page_title="Tax Calculator", layout="centered")

st.title("Tax Calculator")

# User Inputs
basic_salary = st.number_input("Enter Annual Income", min_value=0.0)
hra = st.number_input("Enter hra", min_value=0.0)
other_income = st.number_input("Enter other income", min_value=0.0)


regime = st.selectbox(
    "Select Tax Regime",
    ["Old Regime", "New Regime"]
)

# Calculate Button
if st.button("Calculate Tax"):
    calculator = TaxCalculator(
        basic_salary,
        hra,
        other_income,
        regime
    )

    tax = calculator.calculate_tax()
    st.success(f"✅ Total Tax Payable: ₹ {tax}")