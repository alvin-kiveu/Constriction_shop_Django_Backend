from django.shortcuts import render
from .models import Item, UserProfile
from .serializers import ItemSerializer, UserProfileSerializer
from rest_framework import viewsets

# Create your views here.
class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
