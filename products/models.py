# from django.db import models

# # Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name

# class Item(models.Model):
#     title = models.CharField(max_length=255, null=False, blank=False)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
#     image = models.ImageField(upload_to='uploads/images', null=False, blank=False)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     on_offer = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.title


    

  
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to='uploads/images', null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    on_offer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Professional(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    rating = models.FloatField()

    def __str__(self):
        return self.name
