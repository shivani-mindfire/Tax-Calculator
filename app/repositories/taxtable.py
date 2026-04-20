import sqlite3
from config.log_config import logger
import os


class tax_database:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DB_PATH = os.getenv(
        "DB_PATH",
        os.path.join(BASE_DIR, "repositories", "taxrecord.db")
)
    logger.info(DB_PATH)

    def __init__(self, basic_salary, hra, other_income,gross_income,taxable_income, regime="new"):
        """
        Args:
            basic_salary (float): Basic salary of the individual.
            hra (float): House Rent Allowance of the individual.
            other_income (float): Any other additional income of the individual.
        """
        self.basic_salary = basic_salary
        self.hra = hra
        self.other_income = other_income
        self.regime = regime
        self.taxable_income = taxable_income
        self.gross_income = gross_income
        self.tax_record_tuple = (self.basic_salary,self.hra,self.other_income,self.gross_income,self.regime,self.taxable_income)
    
    def connect(self):
                         
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        tax_table = """CREATE TABLE IF NOT EXISTS TAX_RECORD(TAX_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BASIC_INCOME FLOAT, 
        HRA FLOAT,
        OTHER_INCOME FLOAT,
        GROSS_INCOME FLOAT,
        REGIME VARCHAR(255),
        TAXABLE_INCOME Float
        )"""

        cur.execute(tax_table)
        conn.commit()
        conn.close()
    
    def insertintotable(self):
        logger.info("inserting")

        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        tax_table_data = """INSERT INTO TAX_RECORD
        (BASIC_INCOME, HRA, OTHER_INCOME, GROSS_INCOME,REGIME, TAXABLE_INCOME)
        VALUES(?,?,?,?,?,?)"""
        cur.execute(tax_table_data, self.tax_record_tuple)
        conn.commit()
        conn.close()
        