from django.contrib.auth import get_user_model
from django.db import models

from applications.product.models import Product

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorites', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

