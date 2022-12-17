from django.contrib.auth import get_user_model
from django.db import models

from applications.product.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    order_confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=129)
    confirm_code = models.CharField(max_length=129, default='', null=True, blank=True)

    def create_confirm_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.confirm_code = code
