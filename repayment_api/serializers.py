from rest_framework import serializers
from repayment_api.models import Loan


class RepaymentProfileSerializer(serializers.ModelSerializer):
    """Serializes a repayment profile object"""
    class Meta:
        model = Loan
        fields = '__all__'
