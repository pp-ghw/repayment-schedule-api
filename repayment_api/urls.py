from django.urls import path
from repayment_api import views


urlpatterns = [
    path('', views.RepaymentApiView.as_view()),
    path('<int:pk>/', views.UpdateLoanApiView.as_view()),
]