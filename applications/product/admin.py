from django.contrib import admin

from applications.product.models import Category, Product

admin.site.register(Product)
admin.site.register(Category)
