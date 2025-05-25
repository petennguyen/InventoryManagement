from django.contrib import admin
from .models import InventoryItems, Category

admin.site.register(InventoryItems)
admin.site.register(Category)
