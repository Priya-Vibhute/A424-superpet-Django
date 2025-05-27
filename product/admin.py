from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_name','product_description']

admin.site.register(Product,ProductAdmin)
