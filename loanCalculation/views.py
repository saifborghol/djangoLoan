import numpy_financial as npf
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['POST'])
def calculate_loan_amount(request):
    if request.method == 'POST':
        # Extract data from request
        # int_rate = float(request.POST.get('int_rate'))
        # years = int(request.POST.get('years'))
        # pmts_year = 12
        # monthly_pmt = float(request.POST.get('monthly_pmt'))

        int_rate = float(request.data['int_rate'])
        years = int(request.data['years'])
        pmts_year = 12
        monthly_pmt = float(request.data['monthly_pmt'])
        
        # Calculate loan amount
        loan_amount = npf.pv(int_rate/pmts_year, years*pmts_year, monthly_pmt * -1)
        
        # Create response data
        loan_amount_str = '${0:,.2f}'.format(loan_amount)
        message = 'With a payment of ${0:,.2f}, you can borrow {1}.'.format(monthly_pmt, loan_amount_str)

        data = {
            'loan_amount': loan_amount_str,
            'message': message
        }
        
        # Return response as JSON
        return JsonResponse(data)
    else:
        data = {
            'message': 'error',
            'error_description': 'Invalid request method. Only POST is supported.'
        }
        return JsonResponse(data, status=405)


@api_view(['POST'])
def Payement_Loan_with_fixed_interest_rate(request):
    if request.method == 'POST':
        int_rate = float(request.data['annual_rate'])
        years = int(request.data['years'])
        pmts_year = 12      
        amt_borrowed = float(request.data['loan_amount'])

        # Calculate the monthly payment using Numpy-Financial Library
        payment = npf.pmt(int_rate/pmts_year, years * pmts_year, amt_borrowed)*-1

        # Amount of first payment that goes toward principal (the amount you # borrowed)
        principal_amount = npf.ppmt(int_rate/pmts_year, 1, years*pmts_year, amt_borrowed)*-1

        # Amount of first payment that goes toward interest
        int_amount = npf.ipmt(int_rate/pmts_year, 1, years*pmts_year, amt_borrowed)*-1
        total_pmts = payment * years * pmts_year
        total_int = total_pmts - amt_borrowed
        response_data = {
        'monthly_payment': "${:,.2f}".format(payment),
        'principal_amount': "${:,.2f}".format(principal_amount),
        'interest_amount': "${:,.2f}".format(int_amount),
        '---------------------------':('---------------------------'),
        '':('Assuming all payments are made on time, at the agreed upon amount.'),
        '--------------------------':('---------------------------'),
        'Total principal paid': "${:,.2f}.".format(amt_borrowed),
        'Total interest paid':"${:,.2f}.".format(total_int),
        'Total payments made':"${:,.2f}.".format(total_pmts)

    }
        return JsonResponse(response_data, status=200)
    else:
        data = {
            'message': 'error',
            'error_description': 'Invalid request method.',
        }
        return JsonResponse(data, status=405)
    

@api_view(['POST'])
def Payement_Loan_with_Variable_interest_rate(request):
    if request.method == 'POST':
        loan_amount = float(request.data['loan_amount'])
        interest_rates = [0.05, 0.0575, 0.06]
        loan_duration_years = int(request.data['loan_duration_years'])
        loan_duration_months = loan_duration_years * 12

        y1 = loan_duration_years * 0.25 # first year (25% de la durée du pret)
        y2 = y1 + loan_duration_years * 0.5  # second year 
        y3 = y1 + y2 # third year

        interest1 = interest_rates[0]
        interest2 = interest_rates[1]
        interest3 = interest_rates[2]

        monthly_payment = 0
        for year in range(loan_duration_years):
            if year < y1:
                rate = interest1/12
            elif year < y2:
                rate = interest2/12
            elif year < y3:
                rate = interest3/12
            else:
                rate = interest3/12

        monthly_payment = npf.pmt(rate, loan_duration_months, loan_amount)*-1

        response_data = {
        'monthly_payment': "${:,.2f}".format(monthly_payment)
    }
        return JsonResponse(response_data, status=200)
    else:
        data = {
            'message': 'error',
            'error_description': 'Invalid request method.',
        }
        return JsonResponse(data, status=405)
    

