from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    picture = models.ImageField(upload_to='profile/', blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['joined']