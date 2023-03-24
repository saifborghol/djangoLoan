from django.urls import path
from . import views

urlpatterns = [
    path('loanAmount/', views.calculate_loan_amount, name='loanAmount'),
    path('payementLoanFixedInterestRate/', views.Payement_Loan_with_fixed_interest_rate, name='payementLoanFixedInterestRate'),
    path('payementLoanVariableInterestRate/', views.Payement_Loan_with_Variable_interest_rate, name='payementLoanVariableInterestRate'),
]

