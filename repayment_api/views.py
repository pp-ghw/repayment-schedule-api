from rest_framework.response import Response
from rest_framework import status
from repayment_api.models import Loan, RepaymentSchedules
from repayment_api import serializers
from rest_framework.views import APIView
from dateutil.relativedelta import relativedelta


class RepaymentApiView(APIView):
    """Test API View"""
    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()

    def roundNumber(self, val):
        return round(val,2)

    def calculatePaymentSchedule(self, amount, interest, term, date, id):
        interest = interest/100
        paymentAmount = self.roundNumber(( amount * (interest/12) )/ (1 - (1 + interest/12)**(-12 * term)))
        paymentSchedule = []
        balance = amount
        for i in range(term * 12):
            newInterest =round((interest/12) * balance,2)
            principal = round((paymentAmount - newInterest),2)
            balance = round((balance - principal),2)
            date = date + relativedelta(months=1)

            if balance < 0.1:
                balance = 0

            schedule = {'loan_id': id,'payment_no': i+1, 'date': date, \
                'payment_amount': paymentAmount, 'principal': principal, \
                'interest': newInterest, 'balance': balance, 'updated_at': date.today(), 'date': date.today()}
            
            payment_serializer = serializers.SchedulesSerializer(data=schedule)

            if payment_serializer.is_valid():
                payment_serializer.save()

            paymentSchedule.append(schedule)
        return paymentSchedule


    def get(self, request, pk=None):
        """Returns a list of loans"""
        serializer = self.serializer_class(self.queryset.all(), many=True)
        repayment_serializer = serializers.SchedulesSerializer(RepaymentSchedules.objects.all(), many=True)
        return Response({'loans': serializer.data, 'payment schedules': repayment_serializer.data})

    def post(self, request, pk=None):
        """Create a loan"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            amount = serializer.validated_data.get('loan_amount')
            interest = serializer.validated_data.get('interest_rate')
            term = serializer.validated_data.get('loan_term')
            date = serializer.validated_data.get('created_at')
            serializer.save()
            id = serializer.data.get('id')
            paymentSchedules = self.calculatePaymentSchedule(amount, interest, term, date, id)
            
            return Response({'loan': serializer.data, 'payment schedules': paymentSchedules})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateLoanApiView(APIView):
    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()

    def get(self, request, pk=None):
        """Returns a list of loans"""
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        """Handle updating an object"""
        data = Loan.objects.get(pk=pk)
        serializer = self.serializer_class(instance=data, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        """Delete an object"""
        data = Loan.objects.get(pk=pk)
        data.delete()
        return Response({'message': f"Deleted loan with ID {pk}"})
