from django.db import models
from django.contrib.auth.models import User


class ProductImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product image {self.id}"


class RecognizedProduct(models.Model):
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, related_name="recognized_products")

    name = models.CharField(max_length=255, blank=True, default="")
    category = models.CharField(max_length=120, blank=True, default="")
    confidence = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default="pending")
    nutrition = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.status})"