from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from repayment_api import views


# router = DefaultRouter()
# router.register('', views.RepaymentViewSet, basename='loans')

urlpatterns = [
    path('', views.RepaymentApiView.as_view()),
]