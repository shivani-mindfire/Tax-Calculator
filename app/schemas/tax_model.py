from pydantic import BaseModel

class TaxRequest(BaseModel):
    # id: int
    # basic_salary: float
    # hra: float
    # other_income: float

    basic_salary: float
    hra: float
    other_income: float
    regime: str
    