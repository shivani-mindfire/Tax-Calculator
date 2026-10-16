import streamlit as st
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
# from google import genai
from llms.gemini_llm import explain_tax as explain_tax_gemini
from llms.openai_llm import explain_tax as explain_tax_openai
from llms.groq_llm import compare_regimes as compare_regimes_groq
from llms.ollama_llm import explain_tax as explain_tax_ollama

# Load variables from .env into environment
load_dotenv()

# Access variables using os.getenv()
API_BASE_URL = os.getenv("API_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)


st.set_page_config(page_title="Tax Calculator", layout="wide")
st.title("Tax Calculator")

# ─────────────────────────────────────────────
# Input Fields
# ─────────────────────────────────────────────


with st.sidebar:


    st.subheader("About")
    st.info(
        "This tool helps you calculate income tax under both Old and New regimes "
        "as per Indian Income Tax rules."
    )
    st.caption(" Data is saved via FastAPI backend on port 8000.")



# ─────────────────────────────────────────────
# API Function
# ─────────────────────────────────────────────

def calculate_tax_api(basic_salary, hra, other_income, regime):
    """
    Sends a POST request to the FastAPI /tax endpoint.

    Args:
        basic_salary (float): Basic salary of the individual.
        hra (float): House Rent Allowance.
        other_income (float): Any other additional income.
        regime (str): Tax regime - "Old" or "New".

    Returns:
        dict: API response containing gross_income, taxable_income, total_tax, etc.

    Raises:
        requests.exceptions.ConnectionError: If FastAPI is not running.
        requests.exceptions.HTTPError: If the server returns a 4xx/5xx response.
    """
    payload = {
        "basic_salary": basic_salary,
        "hra": hra,
        "other_income": other_income,
        "regime": regime,
    }
    response = requests.post(f"{API_BASE_URL}/tax", json=payload)
    response.raise_for_status()
    return response.json()


    

col1, col2, col3, col4, col5 = st.columns(5)


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
        
        try:
            result = calculate_tax_api(basic_salary, hra, other_income, regime)

            st.success(f"Tax Payable: ₹ {result['total_tax']:,.2f} |Record saved successfully!")

            st.table({
                "Detail": ["Gross Income", "Taxable Income", "Total Tax"],
                "Amount (₹)": [
                    f"{result['gross_income']:,.2f}",
                    f"{result['taxable_income']:,.2f}",
                    f"{result['total_tax']:,.2f}",
                ]
            })
              # ── GPT-4o Explanation ──────────────────
            with st.spinner("AI is explaining your tax..."):
                # explanation = explain_tax_openai(result)
                # explanation = explain_tax_gemini(result)
                explanation = explain_tax_ollama(result)


            st.subheader("🧾 What does this mean?")
            st.info(explanation)

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI. Make sure it is running on port 8000.")
        except Exception as e:
            st.error(f"Error: {e}")

# ─────────────────────────────────────────────
# Compare Regime Button — local calculation only
# ─────────────────────────────────────────────

if st.button("Compare Regime"):
    st.subheader("Regime Comparison")
    if basic_salary <= 0:
        st.warning("⚠️ Please enter a valid Annual Income.")
    else:
        try:

            old = calculate_tax_api(basic_salary, hra, other_income, "Old")
            new = calculate_tax_api(basic_salary, hra, other_income, "New")

            st.table({
                "Details": ["Gross Income", "Taxable Income", "Tax Payable"],
                "Old Regime (₹)": [
                    f"{old['gross_income']:,.2f}",
                    f"{old['taxable_income']:,.2f}",
                    f"{old['total_tax']:,.2f}",
                ],
                "New Regime (₹)": [
                    f"{new['gross_income']:,.2f}",
                    f"{new['taxable_income']:,.2f}",
                    f"{new['total_tax']:,.2f}",
                ],
            })
            with st.spinner("AI is comparing regimes..."):
                recommendation = compare_regimes_groq(old, new)

            st.subheader("Which Regime is Better for You?")
            st.info(recommendation)


        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI.")
        except Exception as e:
            st.error(f"Error: {e}")
