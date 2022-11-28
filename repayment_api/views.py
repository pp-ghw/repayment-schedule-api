from datetime import datetime
from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from repayment_api import serializers
from repayment_api.models import Loan, RepaymentSchedule

from .helper_functions import calculate_payment_schedule


class RepaymentApiView(APIView):
    """View for GET and POST."""

    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()

    def get(self, request, pk=None):
        """Returns a list of loans"""
        serializer = self.serializer_class(self.queryset.all(), many=True)
        repayment_serializer = serializers.SchedulesSerializer(
            RepaymentSchedule.objects.all(), many=True
        )
        return Response(
            {"loans": serializer.data, "payment schedules": repayment_serializer.data}
        )

    def post(self, request):
        """Create a loan."""
        with transaction.atomic():
            if (
                "loan_amount" in request.data
                and "loan_term" in request.data
                and "interest_rate" in request.data
                and "loan_month" in request.data
                and "loan_year" in request.data
            ):

                loan_amount_decimal = Decimal(request.data["loan_amount"])
                loan_term_int = int(request.data["loan_term"])
                interest_rate_decimal = Decimal(request.data["interest_rate"])
                loan_month = int(request.data["loan_month"])
                loan_year = int(request.data["loan_year"])

                serializer = self.serializer_class(
                    data={
                        "loan_amount": loan_amount_decimal,
                        "loan_term": loan_term_int,
                        "interest_rate": interest_rate_decimal,
                        "loan_year": loan_year,
                        "loan_month": loan_month,
                    }
                )

                if serializer.is_valid():
                    new_loan = Loan(
                        loan_amount=loan_amount_decimal,
                        loan_term=loan_term_int,
                        interest_rate=interest_rate_decimal,
                        loan_year=loan_year,
                        loan_month=loan_month,
                    )
                    new_loan.save()
                    payment_schedules = calculate_payment_schedule(
                        loan_amount_decimal,
                        interest_rate_decimal,
                        loan_term_int,
                        loan_month,
                        loan_year,
                        new_loan,
                    )
                    RepaymentSchedule.objects.bulk_create(payment_schedules)
                    repayments_serializer = serializers.SchedulesSerializer(
                        payment_schedules, many=True
                    ).data

                    return Response(
                        {
                            "loan": serializer.data,
                            "payment schedules": repayments_serializer,
                        }
                    )
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )


class IndividualLoanApiView(APIView):
    """View for retrieve, update and delete."""

    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()

    def get(self, request, pk):
        """Returns a list of loans."""
        data = self.queryset.all().filter(pk=pk)
        serializer = self.serializer_class(data, many=True)
        repayment_schedule = RepaymentSchedule.objects.filter(loan_id__id=pk)
        repayments_serializer = serializers.SchedulesSerializer(
            repayment_schedule, many=True
        ).data

        return Response(
            {"loan": serializer.data, "payment schedules": repayments_serializer}
        )

    def put(self, request, pk):
        """Handle updating an object."""
        try:
            with transaction.atomic():
                loan_amount_decimal = Decimal(request.data["loan_amount"])
                loan_term_int = int(request.data["loan_term"])
                interest_rate_decimal = Decimal(request.data["interest_rate"])
                loan_month = int(request.data["loan_month"])
                loan_year = int(request.data["loan_year"])

                serializer = self.serializer_class(
                    data={
                        "loan_amount": loan_amount_decimal,
                        "loan_term": loan_term_int,
                        "interest_rate": interest_rate_decimal,
                        "loan_year": loan_year,
                        "loan_month": loan_month,
                    },
                    partial=True,
                )

                if serializer.is_valid():
                    repayment_list = RepaymentSchedule.objects.filter(loan_id__id=pk)
                    repayment_list.delete()

                    Loan.objects.filter(pk=pk).update(
                        loan_amount=loan_amount_decimal,
                        loan_term=loan_term_int,
                        interest_rate=interest_rate_decimal,
                        loan_year=loan_year,
                        loan_month=loan_month,
                        updated_at=datetime.now(),
                    )
                    loan_details = Loan.objects.get(id=pk)
                    payment_schedules = calculate_payment_schedule(
                        loan_amount_decimal,
                        interest_rate_decimal,
                        loan_term_int,
                        loan_month,
                        loan_year,
                        loan_details,
                    )
                    RepaymentSchedule.objects.bulk_create(payment_schedules)
                    repayments_serializer = serializers.SchedulesSerializer(
                        payment_schedules, many=True
                    ).data
                    loan_serializer = serializers.LoanSerializer(loan_details).data

                    return Response(
                        {
                            "loan": loan_serializer,
                            "payment schedules": repayments_serializer,
                        }
                    )
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response(str(err), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """Delete an object."""
        data = Loan.objects.get(pk=pk)
        data.delete()
        return Response({"message": f"Deleted loan with ID {pk}"})
