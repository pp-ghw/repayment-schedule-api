from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, date
from django.core.exceptions import ValidationError


class RepaymentProfileManager(BaseUserManager):
    """Manager for repayment profile"""

    def create_repayment(self, loan_amount, loan_term, interest_rate, created_at):
        """Create a new loan """

        loan = self.model(loan_amount=loan_amount, loan_term=loan_term, interest_rate=interest_rate, created_at=created_at)
        loan.save(using=self._db)
        return loan

class RepaymentProfile(AbstractBaseUser):
    """Database model for loans in the sysmte"""
    def validate_date(value):
        if value <= date(2017,1,1) or value >= date(2050,12,31):
            raise ValidationError('Date should be between Jan 2017 - Dec 2050')

    loan_amount = models.IntegerField(validators=[MaxValueValidator(100000000), MinValueValidator(1000)])
    loan_term = models.IntegerField(validators=[MaxValueValidator(50), MinValueValidator(1)])
    interest_rate = models.DecimalField(decimal_places=2, max_digits=4, validators=[MaxValueValidator(50), MinValueValidator(1)])
    created_at = models.DateField(validators=[validate_date])
    updated_at = models.DateField(default=datetime.now())

    objects = RepaymentProfileManager()

    REQUIRED_FIELDS = ['loan_amount', 'loan_term', 'interest_rate', 'created_at']

    def __str__(self):
        """String representation"""
        return {self.loan_amount, self.loan_term, self.interest_rate, self.created_at}
