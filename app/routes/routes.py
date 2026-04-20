
# from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from config.log_config import logger
from schemas.tax_model import TaxRequest
from tax_crud.tax_crud import (
    create_tax,
    get_all,
    get_one,
    update_tax,
    delete_tax,
)

router = APIRouter()


@router.get("/")
def home():
    try:
        logger.info("Home endpoint called")
        return {"message": "Tax Calculator API Running"}
    except Exception as e:
        logger.error(f"Error in home endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/tax")
def create(data: TaxRequest):
    try:
        logger.info(f"Creating tax record with data: {data}")
        return create_tax(data)
    except Exception as e:
        logger.error(f"Error creating tax record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tax")
def read_all():
    try:
        logger.info("Fetching all tax records")
        return get_all()
    except Exception as e:
        logger.error(f"Error fetching records: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tax/{tax_id}")
def read_one(tax_id: int):
    try:
        logger.info(f"Fetching tax record with ID: {tax_id}")
        result = get_one(tax_id)
        if not result:
            logger.warning(f"Tax record not found for ID: {tax_id}")
        return result
    except Exception as e:
        logger.error(f"Error fetching record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tax/{tax_id}")
def update(tax_id: int, data: TaxRequest):
    try:
        logger.info(f"Updating tax record ID: {tax_id} with data: {data}")
        result = update_tax(tax_id, data)
        logger.info(f"Tax record ID: {tax_id} updated successfully")
        return result
    except Exception as e:
        logger.error(f"Error updating record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tax/{tax_id}")
def delete(tax_id: int):
    try:
        logger.warning(f"Deleting tax record with ID: {tax_id}")
        result = delete_tax(tax_id)
        logger.info(f"Tax record ID: {tax_id} deleted successfully")
        return result
    except Exception as e:
        logger.error(f"Error deleting record: {e}")
        raise HTTPException(status_code=500, detail=str(e))