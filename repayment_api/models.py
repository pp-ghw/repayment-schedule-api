from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Loan(models.Model):
    """Database model for loans in the system."""
    def validate_month(value):
        if value<1 or value>12:
            raise ValidationError('Month should be between 1 and 12')
    
    def validate_year(value):
        if value<2017 or value>2050:
            raise ValidationError('Year should be between 2017 and 2050')
    class Meta:
        db_table = 'loan'

    loan_amount = models.DecimalField(decimal_places=6, max_digits=21, validators=[MaxValueValidator(100000000), MinValueValidator(1000)])
    loan_term = models.PositiveIntegerField(validators=[MaxValueValidator(50), MinValueValidator(1)])
    interest_rate = models.DecimalField(decimal_places=6, max_digits=21, validators=[MaxValueValidator(50), MinValueValidator(1)])
    loan_month = models.IntegerField(validators=[validate_month])
    loan_year = models.IntegerField(validators=[validate_year])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation."""
        return f"Loan object {self.id} (loan_amount={self.loan_amount}, loan_term={self.loan_term}, interest_rate={self.interest_rate}, start_date={self.loan_month}/{self.loan_year})"

class RepaymentSchedule(models.Model):
    """Database model for repayment schedules in the system."""
    class Meta:
        db_table = 'repayment_schedule'

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_no = models.PositiveIntegerField()
    payment_amount = models.DecimalField(decimal_places=6, max_digits=21)
    principal = models.DecimalField(decimal_places=6, max_digits=21)
    interest = models.DecimalField(decimal_places=6, max_digits=21)
    balance = models.DecimalField(decimal_places=6, max_digits=21)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    date = models.DateTimeField()

    def __str__(self):
        """String representation."""
        return f"Repayment object {self.payment_no} (payment_amount={self.payment_amount}, principal={self.principal}, interest={self.interest}, balance={self.balance})"
