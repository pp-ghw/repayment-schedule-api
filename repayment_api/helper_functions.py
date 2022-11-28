from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from repayment_api.models import RepaymentSchedule


def round_number(val):
    """Round number to 6 decimal places."""
    return Decimal(val).quantize(Decimal("1.000000"))


def calculate_payment_schedule(amount, interest, term, month, year, loan):
    """Calculate payment schedule."""
    interest_decimal = interest / 100
    pmt = round_number(
        (amount * (interest_decimal / 12))
        / (1 - (1 + interest_decimal / 12) ** (-12 * term))
    )
    payment_schedule = []
    balance = amount
    for i in range(term * 12):
        new_interest_decimal = round_number((interest_decimal / 12) * balance)
        principal = round_number((pmt - new_interest_decimal))
        balance = round_number((balance - principal))
        start_date = datetime(year, int(month), 1) + relativedelta(months=i)

        if i == term * 12 - 1:
            balance = 0

        schedule = RepaymentSchedule(
            loan=loan,
            payment_no=i + 1,
            date=start_date,
            payment_amount=pmt,
            principal=principal,
            interest=new_interest_decimal,
            balance=balance,
        )

        payment_schedule.append(schedule)
    return payment_schedule
