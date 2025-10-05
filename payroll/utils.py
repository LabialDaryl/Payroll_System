from decimal import Decimal

# NOTE: Placeholder computations. Replace with actual PH govt tables/rules.
SSS_RATE = Decimal('0.045')  # placeholder employee share
PHILHEALTH_RATE = Decimal('0.035')  # placeholder shared; use half for employee
PAGIBIG_RATE = Decimal('0.01')  # placeholder employee share capped elsewhere
TAX_RATE = Decimal('0.10')  # placeholder withholding


def compute_contributions(gross: Decimal) -> dict:
    sss = (gross * SSS_RATE).quantize(Decimal('0.01'))
    philhealth = (gross * (PHILHEALTH_RATE / 2)).quantize(Decimal('0.01'))
    pagibig = (gross * PAGIBIG_RATE).quantize(Decimal('0.01'))
    # Simplistic taxable base
    taxable = gross - sss - philhealth - pagibig
    tax = (taxable * TAX_RATE).quantize(Decimal('0.01')) if taxable > 0 else Decimal('0.00')
    net = gross - sss - philhealth - pagibig - tax
    return {
        'sss': sss,
        'philhealth': philhealth,
        'pagibig': pagibig,
        'tax': tax,
        'net': net.quantize(Decimal('0.01')),
    }
