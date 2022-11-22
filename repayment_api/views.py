from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from repayment_api import models
from repayment_api import serializers
from rest_framework.decorators import action


class RepaymentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.RepaymentProfileSerializer
    queryset = models.RepaymentProfile.objects.all()

    @action(methods=["PATCH"], detail=False, url_path="edit")
    def update_loans(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
