from django.contrib import admin

from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price']

    fieldsets = (
        (None, {'fields': ('title', 'description', 'image', 'price', 'featured', 'active')}),
    )

admin.site.register(Product, ProductAdmin)