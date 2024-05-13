from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from stripe.error import StripeError
import stripe
import requests
from products.models import Item
from django.http import JsonResponse
import json
import os
import random



stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckOutView(APIView):
    def post(self, request):

        try:
             # Fetch product and price data from your API
            cart_items = request.data.get('cartItems', [])

            # Extract product and price information
            line_items = []
            for cart in cart_items:
                line_item = {
                    'price_data': {
                        'currency': 'kes',
                        'unit_amount': int(float(cart['price']) * 100),  # Convert price to cents
                        'product_data': {
                            'name': cart['title'],                            
                        },
                    },
                    'quantity': cart['quantity'],
                }
                line_items.append(line_item)

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return Response({'checkout_session_url': checkout_session.url})


        except StripeError as e:
            # Log the specific error
            print(f"Stripe Error: {e}")
            return Response(
                {
                    'error': 'Something went wrong when creating Stripe checkout session'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def generate_random_reference(length=8):
    # Generate a random number with the specified length
    random_number = ''.join(random.choices('123456789', k=length))
    return 'UMS' + random_number

def testrandom(request):
    if request.method == 'GET':
        reference = generate_random_reference()
        return JsonResponse({"reference": reference})


def initiate_stk_push(request):
    if request.method == 'GET':
        # Get the parameters from the query string
        phone = request.GET.get('phone')
        amount = request.GET.get('amount')
        
        # Check if phone and amount are present
        if phone is None or amount is None:
            return JsonResponse({"error": "phone and amount are required in the query string"}, status=400)
        
        print(phone, amount)
        
        # GENERATE A RANDOM REFERENCE NUMBER
        reference = generate_random_reference()
        # GET THE API KEY AND EMAIL FROM THE SETTINGS
        api_key = settings.UMS_PAY_API_KEY
        email = settings.UMS_PAY_EMAIL
        # Process POST request and initiate STK push payment
        # Endpoint URL
        url = "https://api.umeskiasoftwares.com/api/v1/intiatestk"

        # Request headers
        headers = {
            "Content-Type": "application/json"
        }

        # Request payload
        payload = {
            "api_key": api_key,
            "email": email,
            "amount": amount,
            "msisdn": phone,
            "reference": reference
        }

        # Send POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            # Parse response JSON
            data = response.json()
            # Correct the key name here
            return JsonResponse({"success": True, "data": data})
        else:
            return JsonResponse({"success": False, "error": response.text}, status=response.status_code)
    else:
        # CONSOLE TO THE TERMINAL
        print("Method not allowed")
        # Return a method not allowed response for other HTTP methods
        return JsonResponse({"error": "Method not allowed"}, status=405)
      
      


def verify_payment_status(request):
    if request.method == 'GET':
        
        # Get the transaction request ID from the request data
        transaction_request_id = request.GET.get('transaction_request_id')
        print(transaction_request_id)

        # Check if transaction_request_id is present
        if transaction_request_id is None:
            return JsonResponse({"error": "transaction_request_id is required"}, status=400)

        # Get API key and email from settings
        api_key = settings.UMS_PAY_API_KEY
        email = settings.UMS_PAY_EMAIL

        # Endpoint URL for verifying payment status
        url = "https://api.umeskiasoftwares.com/api/v1/transactionstatus"

        # Request payload
        payload = {
            "api_key": api_key,
            "email": email,
            "tranasaction_request_id": transaction_request_id
        }

        # Send POST request to verify payment status
        response = requests.post(url, json=payload)

        # Check if request was successful
        if response.status_code == 200:
            # Parse response JSON
            data = response.json()
            return JsonResponse({"success": True, "data": data})
        else:
            return JsonResponse({"success": False, "error": response.text}, status=response.status_code)
    else:
        # Return a method not allowed response for other HTTP methods
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
        

def ums_pay_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))


        file_path = os.path.join(settings.BASE_DIR, 'ums_pay_transactions.json')
        with open(file_path, 'a+') as json_file:
            json.dump(data, json_file)
            json_file.write('\n')


        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)