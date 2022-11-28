from rest_framework import serializers
from repayment_api.models import Loan, RepaymentSchedule


class LoanSerializer(serializers.ModelSerializer):
    """Serializes a loan object."""
    class Meta:
        model = Loan
        fields = '__all__'

class SchedulesSerializer(serializers.ModelSerializer):
    """Serializes repayment schedule object."""
    class Meta:
        model = RepaymentSchedule
        fields = '__all__'