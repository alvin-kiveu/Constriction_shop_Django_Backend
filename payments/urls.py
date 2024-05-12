from django.urls import path
from .views import StripeCheckOutView
from . import views


urlpatterns = [
    path('create-checkout-session', StripeCheckOutView.as_view()),
    path('initiate-stk-push', views.initiate_stk_push, name='initiate_stk_push'),
    path('ums-pay-callback', views.ums_pay_callback, name='ums_pay_callback'),


]