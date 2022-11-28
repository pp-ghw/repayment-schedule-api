from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.core.exceptions import ValidationError


class Loan(models.Model):
    """Database model for loans in the system"""
    def validate_date(value):
        if value <= date(2017,1,1) or value >= date(2050,12,31):
            raise ValidationError('Date should be between Jan 2017 - Dec 2050')
    class Meta:
        db_table = 'loan'

    loan_amount = models.DecimalField(decimal_places=6, max_digits=21, validators=[MaxValueValidator(100000000), MinValueValidator(1000)])
    loan_term = models.PositiveIntegerField(validators=[MaxValueValidator(50), MinValueValidator(1)])
    interest_rate = models.DecimalField(decimal_places=2, max_digits=4, validators=[MaxValueValidator(50), MinValueValidator(1)])
    loan_month = models.IntegerField()
    loan_year = models.IntegerField()
    created_at = models.DateTimeField(validators=[validate_date], auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation"""
        return {'loan_amount': self.loan_amount, 'loan_term': self.loan_term, 'interest_rate': self.interest_rate, 'created_at': self.created_at}


class RepaymentSchedule(models.Model):
    """Database model for repayment schedules in the system"""
    class Meta:
        db_table = 'repaymentschedule'

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
        """String representation"""
        return {'payment_no': self.payment_no, 'payment_amount': self.payment_amount, 'principal': self.principal, 'interest': self.interest, 'balance': self.balance}
