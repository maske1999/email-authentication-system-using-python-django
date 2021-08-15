from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_varified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)