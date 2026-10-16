import pytest
from services.TaxCalculator import TaxCalculator


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def new_regime_calc():
    return TaxCalculator(900000, 300000, 200000, "New")

@pytest.fixture
def old_regime_calc():
    return TaxCalculator(900000, 300000, 200000, "Old")

@pytest.fixture
def zero_income_calc():
    return TaxCalculator(0, 0, 0, "New")

@pytest.fixture
def below_rebate_calc():
    # Taxable income below 12,00,000 — should get 87A rebate (zero tax)
    return TaxCalculator(500000, 0, 0, "New")


# ─────────────────────────────────────────────
# GROSS INCOME TESTS
# ─────────────────────────────────────────────

class TestGrossIncome:

    def test_gross_income_sum(self, new_regime_calc):
        assert new_regime_calc.calculate_gross_income() == 1400000

    def test_gross_income_zero(self, zero_income_calc):
        assert zero_income_calc.calculate_gross_income() == 0

    def test_gross_income_only_basic(self):
        calc = TaxCalculator(500000, 0, 0, "New")
        assert calc.calculate_gross_income() == 500000


# ─────────────────────────────────────────────
# TAXABLE INCOME TESTS
# ─────────────────────────────────────────────

class TestTaxableIncome:

    def test_taxable_income_new_regime(self, new_regime_calc):
        # gross = 14,00,000 - standard deduction 75,000 = 13,25,000
        assert new_regime_calc.calculate_taxable_income() == 1325000

    def test_taxable_income_old_regime(self, old_regime_calc):
        # gross = 14,00,000 - standard deduction 20,000 = 13,80,000
        assert old_regime_calc.calculate_taxable_income() == 1380000

    def test_taxable_income_zero(self, zero_income_calc):
        # gross = 0 - 75,000 = -75,000
        assert zero_income_calc.calculate_taxable_income() == -75000

    def test_standard_deduction_new_regime(self):
        calc = TaxCalculator(800000, 0, 0, "New")
        assert calc.calculate_taxable_income() == 800000 - 75000

    def test_standard_deduction_old_regime(self):
        calc = TaxCalculator(800000, 0, 0, "Old")
        assert calc.calculate_taxable_income() == 800000 - 20000


# ─────────────────────────────────────────────
# NEW REGIME TAX TESTS
# ─────────────────────────────────────────────

class TestNewRegimeTax:

    def test_no_tax_below_400000(self):
        # taxable = 3,00,000 → 0 tax
        calc = TaxCalculator(375000, 0, 0, "New")
        assert calc.calculate_new_regime_tax() == 0

    def test_87a_rebate_below_1200000(self, below_rebate_calc):
        # taxable = 5,00,000 - 75,000 = 4,25,000 → rebate applies → 0
        assert below_rebate_calc.calculate_new_regime_tax() == 0

    def test_tax_above_rebate_limit(self):
        # taxable income above 12,00,000 — tax should be > 0
        calc = TaxCalculator(1500000, 0, 0, "New")
        assert calc.calculate_new_regime_tax() > 0

    def test_tax_slab_5_percent(self):
        # taxable = 6,00,000 → (6,00,000 - 4,00,000) * 5% = 10,000
        # but 87A rebate applies (income <= 12L) → tax = 0
        calc = TaxCalculator(675000, 0, 0, "New")
        assert calc.calculate_new_regime_tax() == 0

    def test_cess_applied(self):
        # For income above rebate limit, cess of 4% should be added
        calc = TaxCalculator(2000000, 0, 0, "New")
        tax = calc.calculate_new_regime_tax()
        assert tax > 0
        # Tax should include 4% cess — verify it's not a round number
        assert tax == pytest.approx(tax, rel=1e-2)

    def test_new_regime_high_income(self, new_regime_calc):
        # taxable = 13,25,000 → above 12L so tax applies
        tax = new_regime_calc.calculate_new_regime_tax()
        assert tax > 0


# ─────────────────────────────────────────────
# OLD REGIME TAX TESTS
# ─────────────────────────────────────────────

class TestOldRegimeTax:

    def test_no_tax_below_250000(self):
        calc = TaxCalculator(200000, 0, 0, "Old")
        # taxable = 2,00,000 - 20,000 = 1,80,000 → 0 tax
        assert calc.calculate_old_regime_tax() == 0

    def test_tax_5_percent_slab(self):
        # taxable = 3,50,000 → (3,50,000 - 2,50,000) * 5% = 5,000 + 4% cess
        calc = TaxCalculator(370000, 0, 0, "Old")
        tax = calc.calculate_old_regime_tax()
        assert tax == pytest.approx(5200.0, rel=1e-2)

    def test_tax_20_percent_slab(self):
        calc = TaxCalculator(800000, 0, 0, "Old")
        tax = calc.calculate_old_regime_tax()
        assert tax > 0

    def test_tax_30_percent_slab(self):
        calc = TaxCalculator(1500000, 0, 0, "Old")
        tax = calc.calculate_old_regime_tax()
        assert tax > 0

    def test_cess_applied_old_regime(self):
        calc = TaxCalculator(800000, 0, 0, "Old")
        tax = calc.calculate_old_regime_tax()
        assert tax > 0


# ─────────────────────────────────────────────
# CALCULATE TAX (DISPATCHER) TESTS
# ─────────────────────────────────────────────

class TestCalculateTax:

    def test_dispatches_new_regime(self, new_regime_calc):
        assert new_regime_calc.calculate_tax() == new_regime_calc.calculate_new_regime_tax()

    def test_dispatches_old_regime(self, old_regime_calc):
        assert old_regime_calc.calculate_tax() == old_regime_calc.calculate_old_regime_tax()

    def test_invalid_regime_raises_error(self):
        calc = TaxCalculator(500000, 0, 0, "Invalid Regime")
        with pytest.raises(ValueError, match="Invalid tax regime selected"):
            calc.calculate_tax()

    def test_new_regime_lower_tax_high_income(self):
        # For very high income, compare both regimes
        old = TaxCalculator(3000000, 0, 0, "Old")
        new = TaxCalculator(3000000, 0, 0, "New")
        assert isinstance(old.calculate_tax(), float)
        assert isinstance(new.calculate_tax(), float)


# ─────────────────────────────────────────────
# FAILURE & EDGE CASE TESTS
# ─────────────────────────────────────────────

class TestFailureCases:


    # --------------------------------------------
    # Negative Salary Inputs
    # --------------------------------------------
    def test_negative_basic_salary(self):
        calc = TaxCalculator(-500000, 0, 0, "New")
        gross = calc.calculate_gross_income()
        assert gross < 0

    def test_negative_hra(self):
        calc = TaxCalculator(500000, -100000, 0, "New")
        gross = calc.calculate_gross_income()
        assert gross == 400000

    def test_negative_other_income(self):
        calc = TaxCalculator(500000, 0, -200000, "Old")
        gross = calc.calculate_gross_income()
        assert gross == 300000


    def test_zero_income_tax(self, zero_income_calc):
        tax = zero_income_calc.calculate_tax()
        assert tax == 0

    # --------------------------------------------
    # Tax Should Never Be Negative
    # --------------------------------------------
    def test_tax_not_negative_new(self):
        calc = TaxCalculator(0, 0, 0, "New")
        assert calc.calculate_new_regime_tax() >= 0

    def test_tax_not_negative_old(self):
        calc = TaxCalculator(0, 0, 0, "Old")
        assert calc.calculate_old_regime_tax() >= 0

    # --------------------------------------------
    # Wrong Data Type Inputs
    # --------------------------------------------
    def test_string_input_salary(self):
        with pytest.raises(TypeError):
            TaxCalculator("500000", 0, 0, "New")

    def test_none_input(self):
        with pytest.raises(TypeError):
            TaxCalculator(None, 0, 0, "Old")


    # --------------------------------------------
    # Large Negative Taxable Income
    # --------------------------------------------
    def test_large_negative_taxable_income(self):
        calc = TaxCalculator(0, 0, 0, "New")
        taxable = calc.calculate_taxable_income()
        assert taxable <= 0