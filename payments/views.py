from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from stripe.error import StripeError
import stripe
import requests
from products.models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckOutView(APIView):
    def post(self, request):

        try:
             # Fetch product and price data from your API
            product_data = requests.get('http://127.0.0.1:8000/api/items/')
            products = product_data.json()

            # Extract product and price information
            line_items = []
            for product in products:
                line_item = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(product['price']) * 100),  # Convert price to cents
                        'product_data': {
                            'name': product['title'],
                            'description': product['description'],
                            'images': [product['image']],
                        },
                    },
                    'quantity': 1,
                }
                line_items.append(line_item)

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return redirect(checkout_session.url)

        except StripeError as e:
            # Log the specific error
            print(f"Stripe Error: {e}")
            return Response(
                {
                    'error': 'Something went wrong when creating Stripe checkout session'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

