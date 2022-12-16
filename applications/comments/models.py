from django.contrib.auth import get_user_model
from django.db import models

from applications.product.models import Product

User = get_user_model()


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
