from django.shortcuts import render
from .models import Item
from .serializers import ItemSerializer, CategorySerializer
from rest_framework import viewsets

# Create your views here.
class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ItemSerializer
        return CategorySerializer

    
