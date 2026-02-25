from django.contrib import admin
from .models import ProductImage, RecognizedProduct

admin.site.register(ProductImage)
admin.site.register(RecognizedProduct)