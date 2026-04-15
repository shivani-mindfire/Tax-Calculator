from schema.tax_model import TaxRequest
from services.TaxCalculator import TaxCalculator
from config.log_config import logger


tax_db = {}


# CREATE
def create_tax(data: TaxRequest):
    logger.info(f"Creating tax record for ID: {data.id}")
    calc = TaxCalculator(
        data.basic_salary,
        data.hra,
        data.other_income
    )
    result = {
        "id": data.id,
        "basic_salary": data.basic_salary,
        "hra": data.hra,
        "other_income": data.other_income,
        "gross_income": calc.calculate_gross_income(),        
        "taxable_income": calc.calculate_taxable_income(),    
        "total_tax": calc.calculate_tax()                     
    }
    tax_db[data.id] = result
    logger.info(f"Tax record created successfully | ID: {data.id} | Gross: {result['gross_income']} | Tax: {result['total_tax']}")
    return result

# READ ALL
def get_all():
    logger.info(f"Fetching all tax records | Total records: {len(tax_db)}")
    return tax_db

# READ ONE
def get_one(tax_id: int):
    logger.info(f"Fetching tax record for ID: {tax_id}")
    record = tax_db.get(tax_id)
    if record:
        logger.info(f"Tax record found for ID: {tax_id}")
    else:
        logger.warning(f"Tax record NOT found for ID: {tax_id}")
    return record

# UPDATE
def update_tax(tax_id: int, data: TaxRequest):
    logger.info(f"Updating tax record for ID: {tax_id}")
    if tax_id in tax_db:
        calc = TaxCalculator(
            data.basic_salary,
            data.hra,
            data.other_income
        )
        result = {
            "id": tax_id,
            "basic_salary": data.basic_salary,
            "hra": data.hra,
            "other_income": data.other_income,
            "gross_income": calc.calculate_gross_income(),
            "taxable_income": calc.calculate_taxable_income(),
            "total_tax": calc.calculate_tax()
        }
        tax_db[tax_id] = result
        logger.info(f"Tax record updated successfully | ID: {tax_id} | New Tax: {result['total_tax']}")
        return result
    logger.error(f"Update failed — Tax record NOT found for ID: {tax_id}")
    return {"error": "Not found"}

# DELETE
def delete_tax(tax_id: int):
    logger.warning(f"Attempting to delete tax record for ID: {tax_id}")
    return tax_db.pop(tax_id, {"error": "Not found"})