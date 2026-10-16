import ollama
from config.env_config import settings


def explain_tax(result: dict) -> str:
    """
    Explains a single tax calculation in simple language using Ollama (LLaMA 3.2).

    Args:
        result (dict): Tax result containing gross_income,
                       taxable_income, total_tax, regime.

    Returns:
        str: Plain-English explanation from LLaMA 3.2 via Ollama (local).
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
    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def compare_regimes(old: dict, new: dict) -> str:
    """
    Compares Old vs New tax regime and recommends the better one.

    Args:
        old (dict): Tax result for Old regime containing
                    gross_income, taxable_income, total_tax.
        new (dict): Tax result for New regime containing
                    gross_income, taxable_income, total_tax.

    Returns:
        str: Plain-English comparison and recommendation from LLaMA 3.2.
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
    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]