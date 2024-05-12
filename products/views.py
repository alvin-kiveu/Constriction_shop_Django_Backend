from django.shortcuts import render
from .models import Item
from .serializers import ItemSerializer, CategorySerializer
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from .models import Professional
from django.http import JsonResponse


# Create your views here.
class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    
    @extend_schema(responses=ItemSerializer)
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ItemSerializer
        return CategorySerializer



def professionals(request):
    # Retrieve list of professions from the database
    professions = Professional.objects.all()
    
    # Pass professions to the template
    return render(request, 'professionals.html', {'professions': professions})






