# import logging
from config.log_config import logger


class TaxCalculator:
    """
    A class to calculate income tax based on Indian tax slabs.

    Args:
        STANDARD_DEDUCTION (int): Fixed standard deduction amount = 50,000.
        basic_salary (float): Basic salary of the individual.
        hra (float): House Rent Allowance of the individual.
        other_income (float): Any other additional income.
    """
    STANDARD_DEDUCTION = 50000
    logger.info("Application started")
    logger.info(STANDARD_DEDUCTION)

    
    def __init__(self, basic_salary, hra, other_income, regime):
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
        # logger.info(f"TaxCalculator initialized | Basic: {basic_salary} | HRA: {hra} | Other: {other_income}")


    def calculate_gross_income(self):
        """
        Calculates the total gross income by summing all income components.
        """
        gross = self.basic_salary + self.hra + self.other_income
        # logger.info(f"Gross income calculated: {gross}")
        return gross

    def calculate_taxable_income(self):
        """
        Calculates taxable income after applying standard deduction.
        """

        if self.regime == "new":
            self.STANDARD_DEDUCTION = 75000
        else:
            self.STANDARD_DEDUCTION = 50000

        gross_income = self.calculate_gross_income()
        taxable_income = gross_income - self.STANDARD_DEDUCTION
        # logger.info(f"Taxable income calculated: {taxable_income} (after deduction of {self.STANDARD_DEDUCTION})")
        return taxable_income

    def calculate_new_regime_tax(self):
        """
        Calculates total income tax based on Indian new tax regime slabs.

        Tax Slabs:
            - Up to 4,00,000        : No tax (0%)
            - 4,00,001 - 8,00,000   : 5%
            - 8,00,001 - 12,00,000   : 10%
            - 12,00,001 - 16,00,000  : 15%
            - 16,00,001 - 20,00,000 : 20%
            - Above 20,00,000       : 30%
        """
        income = self.calculate_taxable_income()
        tax = 0

        if income <= 400000:
            tax = 0

        elif income <= 800000:
            tax = (income - 400000) * 0.05

        elif income <= 1200000:
            tax = 15000 + (income - 800000) * 0.10

        elif income <= 1600000:
            tax = 60000 + (income - 1200000) * 0.15

        elif income <= 2000000:
            tax = 120000 + (income - 1600000) * 0.20

        elif income <= 2400000:
            tax = 200000 + (income - 2400000) * 0.25

        else:
            tax = 300000 + (income - 2400000) * 0.30
        # ⭐ Section 87A Rebate
        if income <= 1200000:
            tax = 0

        # Add 4% Health & Education Cess
        cess = tax * 0.04
        tax = tax + cess
        
        # logger.info(f"Tax calculated: {tax} for taxable income: {income}")

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

        # Add 4% Health & Education Cess
        cess = tax * 0.04
        tax = tax + cess
        # logger.info(f"TaxCalculator initialized | Basic: {self.basic_salary} | HRA: {self.hra} | Other: {self.other_income}")
        
        return tax

    def calculate_tax(self):

        # income = self.calculate_taxable_income()
        
        if self.regime == "new":
            tax = self.calculate_new_regime_tax()

        elif self.regime == "old":
            tax = self.calculate_old_regime_tax()

        else:
            raise ValueError("Invalid tax regime selected")


        # logger.info(
            # f"Tax calculated: {tax} | Regime: {self.regime} | "
        # )

        return tax
    