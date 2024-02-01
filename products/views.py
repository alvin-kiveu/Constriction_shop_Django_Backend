from django.shortcuts import render
from .models import Item
from .serializers import ItemSerializer
from rest_framework import viewsets

# Create your views here.
class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


    
