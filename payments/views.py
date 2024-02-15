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

