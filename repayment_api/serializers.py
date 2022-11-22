from rest_framework import serializers
from repayment_api import models


class RepaymentProfileSerializer(serializers.ModelSerializer):
    """Serializes a repayment profile object"""
    class Meta:
        model = models.RepaymentProfile
        fields = ('id', 'loan_amount', 'loan_term', 'interest_rate', 'created_at')

    def create(self, validated_data):
        """create and return a new repayment schedule"""
        repayment = models.RepaymentProfile.objects.create_repayment(
            loan_amount=validated_data['loan_amount'],
            loan_term=validated_data['loan_term'],
            interest_rate=validated_data['interest_rate'],
            created_at=validated_data['created_at']
        )
        return repayment
