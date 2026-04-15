# import logging
from config.log_config import logger


class TaxCalculator:
    """
    A class to calculate income tax based on Indian tax slabs.

    Attributes:
        STANDARD_DEDUCTION (int): Fixed standard deduction amount = 50,000.
        basic_salary (float): Basic salary of the individual.
        hra (float): House Rent Allowance of the individual.
        other_income (float): Any other additional income.
    """
    STANDARD_DEDUCTION = 50000
    logger.info("Application started")
    
    def __init__(self, basic_salary, hra, other_income, regime="new regime"):
        """
        Initializes TaxCalculator with salary components.

        Args:
            basic_salary (float): Basic salary of the individual.
            hra (float): House Rent Allowance of the individual.
            other_income (float): Any other additional income of the individual.
        """
        self.basic_salary = basic_salary
        self.hra = hra
        self.other_income = other_income
        self.regime = regime.lower()
        logger.info(f"TaxCalculator initialized | Basic: {basic_salary} | HRA: {hra} | Other: {other_income}")


    def calculate_gross_income(self):
        """
        Calculates the total gross income by summing all income components.
        """
        gross = self.basic_salary + self.hra + self.other_income
        logger.info(f"Gross income calculated: {gross}")
        return gross

    def calculate_taxable_income(self):
        """
        Calculates taxable income after applying standard deduction.
        """
        gross_income = self.calculate_gross_income()
        taxable_income = gross_income - self.STANDARD_DEDUCTION
        logger.info(f"Taxable income calculated: {taxable_income} (after deduction of {self.STANDARD_DEDUCTION})")
        return taxable_income

    def calculate_new_regime_tax(self):
        """
        Calculates total income tax based on Indian new tax regime slabs.

        Tax Slabs:
            - Up to 3,00,000        : No tax (0%)
            - 3,00,001 - 6,00,000   : 5%
            - 6,00,001 - 9,00,000   : 10%
            - 9,00,001 - 12,00,000  : 15%
            - 12,00,001 - 15,00,000 : 20%
            - Above 15,00,000       : 30%
        """
        income = self.calculate_taxable_income()
        tax = 0

        if income <= 300000:
            tax = 0

        elif income <= 600000:
            tax = (income - 300000) * 0.05

        elif income <= 900000:
            tax = 15000 + (income - 600000) * 0.10

        elif income <= 1200000:
            tax = 45000 + (income - 900000) * 0.15

        elif income <= 1500000:
            tax = 90000 + (income - 1200000) * 0.20

        else:
            tax = 150000 + (income - 1500000) * 0.30
        logger.info(f"Tax calculated: {tax} for taxable income: {income}")

        return tax
    
    
    
    def calculate_old_regime_tax(self):
        income = self.calculate_taxable_income()

        if income <= 250000:
            tax = 0

        elif income <= 500000:
            tax = (income - 250000) * 0.05

        elif income <= 1000000:
            tax = 12500 + (income - 500000) * 0.20

        else:
            tax = 112500 + (income - 1000000) * 0.30

        return tax

    def calculate_tax(self):

        income = self.calculate_taxable_income()
        
        if self.regime == "new regime":
            tax = self.calculate_new_regime_tax()

        elif self.regime == "old regime":
            tax = self.calculate_old_regime_tax()

        else:
            raise ValueError("Invalid tax regime selected")


        logger.info(
            f"Tax calculated: {tax} | Regime: {self.regime} | Income: {income}"
        )

        return tax
    

# basic = float(input("Enter Basic Salary: "))
# hra = float(input("Enter HRA: "))
# other = float(input("Enter Other Income: "))

# tax_obj = TaxCalculator(basic, hra, other)

# print("Gross Income:", tax_obj.calculate_gross_income())
# print("Taxable Income:", tax_obj.calculate_taxable_income())
# print("Total Tax:", tax_obj.calculate_tax())