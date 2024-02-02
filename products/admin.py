from django.contrib import admin
from .models import Category, Item

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'on_offer')
    list_filter = ('category', 'on_offer')

admin.site.register(Item, ItemAdmin)




