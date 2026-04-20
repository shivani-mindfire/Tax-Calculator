import streamlit as st
import requests
from services.TaxCalculator import TaxCalculator
# import os
API_BASE_URL = "http://localhost:8000"

# API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Tax Calculator", layout="centered")
st.title("Tax Calculator")

# ─────────────────────────────────────────────
# Input Fields
# ─────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
    # record_id = st.number_input("Record ID", min_value=1, step=1)

with col1:
    basic_salary = st.number_input("Annual Income (₹)", min_value=0.0)

with col2:
    hra = st.number_input("HRA (₹)", min_value=0.0)

with col3:
    other_income = st.number_input("Other Income (₹)", min_value=0.0)

with col4:
    regime = st.selectbox("Tax Regime", ["New", "Old"])

# ─────────────────────────────────────────────
# Calculate Tax Button — sends data via FastAPI
# ─────────────────────────────────────────────

if st.button("Calculate Tax"):
    if basic_salary <= 0:
        st.warning(" Please enter a valid Annual Income.")
    else:
        calculator = TaxCalculator(basic_salary, hra, other_income, regime)
        gross_income = calculator.calculate_gross_income()
        tax = calculator.calculate_tax()
        payload = {
            
            "basic_salary": basic_salary,
            "hra": hra,
            "other_income": other_income,
            "gross_income": gross_income,
            "tax": tax,
            "regime": regime,
        }
        try:
            response = requests.post(f"{API_BASE_URL}/tax", json=payload)
            response.raise_for_status()
            result = response.json()

            st.success(f"Tax Payable: ₹ {result['total_tax']:,.2f} |Record saved successfully!")

            st.table({
                "Detail": ["Gross Income", "Taxable Income", "Total Tax"],
                "Amount (₹)": [
                    f"{result['gross_income']:,.2f}",
                    f"{result['taxable_income']:,.2f}",
                    f"{result['total_tax']:,.2f}",
                ]
            })

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI. Make sure it is running on port 8000.")
        except Exception as e:
            st.error(f"Error: {e}")

# ─────────────────────────────────────────────
# Compare Regime Button — local calculation only
# ─────────────────────────────────────────────

if st.button("Compare Regime"):
    old = TaxCalculator(basic_salary, hra, other_income, "Old")
    new = TaxCalculator(basic_salary, hra, other_income, "New")

    st.subheader("Regime Comparison")
    st.table({
        "Details": ["Gross Income", "Taxable Income", "Tax Payable"],
        "Old Regime (₹)": [
            f"{old.calculate_gross_income():,.2f}",
            f"{old.calculate_taxable_income():,.2f}",
            f"{old.calculate_tax():,.2f}",
        ],
        "New Regime (₹)": [
            f"{new.calculate_gross_income():,.2f}",
            f"{new.calculate_taxable_income():,.2f}",
            f"{new.calculate_tax():,.2f}",
        ],
    })