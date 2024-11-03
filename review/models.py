from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from journey.models import Journey


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewee')
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    comment = models.CharField(max_length=200)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.rating + ' by ' + self.reviewer.username + ' for ' + self.reviewee.username
    
    class Meta:
        ordering = ['-reviewed_at']
        
    