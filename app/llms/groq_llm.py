import os
from groq import Groq
from dotenv import load_dotenv
from config.env_config import settings

load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

client = Groq(api_key=settings.GROQ_API_KEY)



def compare_regimes(old: dict, new: dict) -> str:
    """
    Compares Old vs New tax regime and recommends the better one.

    Args:
        old (dict): Tax result for Old regime containing
                    gross_income, taxable_income, total_tax.
        new (dict): Tax result for New regime containing
                    gross_income, taxable_income, total_tax.

    Returns:
        str: Plain-English comparison and recommendation from LLaMA3.
    """
    savings = abs(old['total_tax'] - new['total_tax'])
    better  = "Old" if old['total_tax'] < new['total_tax'] else "New"

    prompt = f"""
    You are a friendly Indian tax advisor. Compare the following two tax regimes 
    and clearly tell which one is better for this person and why.
    Use bullet points, keep it simple and concise.

    Old Regime:
    - Taxable Income : ₹{old['taxable_income']:,.2f}
    - Total Tax      : ₹{old['total_tax']:,.2f}

    New Regime:
    - Taxable Income : ₹{new['taxable_income']:,.2f}
    - Total Tax      : ₹{new['total_tax']:,.2f}

    Key Facts:
    - The {better} Regime saves ₹{savings:,.2f} in tax
    - Gross Income is ₹{old['gross_income']:,.2f} (same for both)

    Please:
    1. Clearly state which regime is better and by how much
    2. Explain why in simple terms
    3. Give a final recommendation
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )
    return response.choices[0].message.content