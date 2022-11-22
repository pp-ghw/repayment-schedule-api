from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.core.exceptions import ValidationError


class Loan(models.Model):
    """Database model for loans in the system"""
    def validate_date(value):
        if value <= date(2017,1,1) or value >= date(2050,12,31):
            raise ValidationError('Date should be between Jan 2017 - Dec 2050')

    loan_amount = models.IntegerField(validators=[MaxValueValidator(100000000), MinValueValidator(1000)])
    loan_term = models.IntegerField(validators=[MaxValueValidator(50), MinValueValidator(1)])
    interest_rate = models.DecimalField(decimal_places=2, max_digits=4, validators=[MaxValueValidator(50), MinValueValidator(1)])
    created_at = models.DateField(validators=[validate_date])
    updated_at = models.DateField(blank=True)


    def __str__(self):
        """String representation"""
        return {self.loan_amount, self.loan_term, self.interest_rate, self.created_at}
