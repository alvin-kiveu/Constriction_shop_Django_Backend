from django.db import models

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to='uploads/images', null=False, blank=False)
    category = models.CharField(max_length=255,null=True, blank=True)
    on_offer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


    

  
