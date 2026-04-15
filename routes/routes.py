
# from fastapi import APIRouter
from fastapi import APIRouter
from config.log_config import logger
from schema.tax_model import TaxRequest
from crud.tax_crud import (
    create_tax,
    get_all,
    get_one,
    update_tax,
    delete_tax,
)

router = APIRouter()


@router.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message": "Tax Calculator API Running"}


@router.post("/tax")
def create(data: TaxRequest):
    logger.info(f"Creating tax record with data: {data}")
    return create_tax(data)


@router.get("/tax")
def read_all():
    logger.info("Fetching all tax records")
    return get_all()


@router.get("/tax/{tax_id}")
def read_one(tax_id: int):
    logger.info(f"Fetching tax record with ID: {tax_id}")
    result = get_one(tax_id)
    if not result:
        logger.warning(f"Tax record not found for ID: {tax_id}")
    return result


@router.put("/tax/{tax_id}")
def update(tax_id: int, data: TaxRequest):
    logger.info(f"Updating tax record ID: {tax_id} with data: {data}")
    result = update_tax(tax_id, data)
    logger.info(f"Tax record ID: {tax_id} updated successfully")
    return result


@router.delete("/tax/{tax_id}")
def delete(tax_id: int):
    logger.warning(f"Deleting tax record with ID: {tax_id}")
    result = delete_tax(tax_id)
    logger.info(f"Tax record ID: {tax_id} deleted successfully")
    return result