import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_tax(result: dict) -> str:
    """
    Explains tax calculation in simple language using GPT via OpenAI.

    Args:
        result (dict): Tax result containing gross_income,
                       taxable_income, total_tax, regime.

    Returns:
        str: Plain-English explanation from GPT.
    """
    prompt = f"""
    You are a friendly Indian tax advisor. Explain the following tax calculation 
    in very simple language that anyone can understand. Use bullet points, 
    avoid jargon, and keep it concise.

    Tax Details:
    - Regime        : {result['regime']}
    - Gross Income  : ₹{result['gross_income']:,.2f}
    - Taxable Income: ₹{result['taxable_income']:,.2f}
    - Total Tax     : ₹{result['total_tax']:,.2f}

    Explain:
    1. How the taxable income was arrived at from gross income
    2. Which tax slab applied and why
    3. What the final tax amount means in simple terms
    """
    response = client.responses.create(
        model="gpt-4o",
        input=[{"role": "user", "content": prompt}],
    )
    return response.output_text