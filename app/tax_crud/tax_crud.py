import sqlite3
from schemas.tax_model import TaxRequest
from services.TaxCalculator import TaxCalculator
from repositories.taxtable import tax_database
from config.log_config import logger


def get_connection():
    """Get SQLite connection using same DB_PATH as tax_database class."""
    conn = sqlite3.connect(tax_database.DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create table if it doesn't exist."""
    db = tax_database(0, 0, 0, 0, 0)
    db.connect()


# Run on startup
init_db()


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────
def create_tax(data: TaxRequest):
    logger.info(f"Creating tax")

    calc = TaxCalculator(data.basic_salary, data.hra, data.other_income)
    gross_income    = calc.calculate_gross_income()
    taxable_income  = calc.calculate_taxable_income()
    total_tax       = calc.calculate_tax()

    db = tax_database(
        data.basic_salary,
        data.hra,
        data.other_income,
        gross_income,
        taxable_income,
        data.regime
    )
    db.connect()
    db.insertintotable()

    logger.info(f"Record inserted into SQLite | Gross: {gross_income} | Tax: {total_tax}")

    return {
        "basic_salary":   data.basic_salary,
        "hra":            data.hra,
        "other_income":   data.other_income,
        "gross_income":   gross_income,
        "taxable_income": taxable_income,
        "total_tax":      total_tax,
        "regime":         data.regime,
    }


# ─────────────────────────────────────────────
# READ ALL
# ─────────────────────────────────────────────
def get_all():
    import sqlite3
    conn = sqlite3.connect(tax_database.DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TAX_RECORD")
    rows = cur.fetchall()
    conn.close()
    logger.info(f"Fetched {len(rows)} records")
    return [dict(row) for row in rows]



# READ ONE
def get_one(tax_id: int):
    import sqlite3
    conn = sqlite3.connect(tax_database.DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TAX_RECORD WHERE TAX_ID = ?", (tax_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        logger.info(f"Record found for ID: {tax_id}")
        return dict(row)
    logger.warning(f"Record NOT found for ID: {tax_id}")
    return {"error": "Not found"}


# UPDATE
def update_tax(tax_id: int, data: TaxRequest):
    import sqlite3
    calc = TaxCalculator(data.basic_salary, data.hra, data.other_income, data.regime)
    taxable_income = calc.calculate_taxable_income()

    conn = sqlite3.connect(tax_database.DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE TAX_RECORD
        SET BASIC_INCOME   = ?,
            HRA            = ?,
            OTHER_INCOME   = ?,
            GROSS_INCOME   = ?,
            REGIME         = ?,
            TAXABLE_INCOME = ?
        WHERE TAX_ID = ?
    """, (data.basic_salary, data.hra, data.other_income,
          data.gross_income, data.regime, taxable_income, tax_id))
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        logger.error(f"Update failed — ID {tax_id} not found")
        return {"error": "Not found"}

    conn.close()
    logger.info(f"Record {tax_id} updated")
    return get_one(tax_id)


# DELETE
def delete_tax(tax_id: int):
    import sqlite3
    conn = sqlite3.connect(tax_database.DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM TAX_RECORD WHERE TAX_ID = ?", (tax_id,))
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        logger.warning(f"Delete failed — ID {tax_id} not found")
        return {"error": "Not found"}

    conn.close()
    logger.info(f"Record {tax_id} deleted")
    return {"message": f"Record {tax_id} deleted successfully"}