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


def initiate_stk_push(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        msisdn = request.POST.get('msisdn')
        reference = request.POST.get('reference')

        # Endpoint URL
        url = "https://api.umeskiasoftwares.com/api/v1/intiatestk"

        # Request headers
        headers = {
            "Content-Type": "application/json"
        }

        # Request payload
        payload = {
            "api_key": "VE5MTlkzRk06MTlwNjlkZWM=",
            "email": "example@gmail.com",
            "amount": amount,
            "msisdn": msisdn,
            "reference": reference
        }

        # Send POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            # Parse response JSON
            data = response.json()
            return JsonResponse({"success": True, "transaction_request_id": data["tranasaction_request_id"]})
        else:
            return JsonResponse({"success": False, "error": response.text}, status=response.status_code)


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