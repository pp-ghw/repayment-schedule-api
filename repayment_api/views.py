from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from repayment_api.models import Loan
from repayment_api import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView


class RepaymentApiView(APIView):
    """Test API View"""
    serializer_class = serializers.RepaymentProfileSerializer
    queryset = Loan.objects.all()

    def get(self, request, format=None):
        """Returns a list of loans"""
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a loan"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'loan': serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        # item = self.queryset.all().get(pk=pk)
        item = Loan.objects.get(pk=pk)
        data = self.serializer_class(item, data=request.data)
        return Response({item, data})
        # if data.is_valid():
        #     data.save()
        #     return Response(data.data)
        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

class RepaymentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.RepaymentProfileSerializer
    queryset = Loan.objects.all()

    @action(methods=["PATCH"], detail=False, url_path="edit")
    def update_loans(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
