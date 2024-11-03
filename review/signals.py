from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Avg


def update_avg_rating(reviewee):
    average_rating = Review.objects.filter(reviewee=reviewee).aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    if average_rating is not None:
        average_rating = Decimal(average_rating).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    else:
        average_rating = Decimal("0.00")

    reviewee.avg_rating = average_rating
    reviewee.save()


@receiver(post_save, sender=Review)
def update_avg_on_save(sender, instance, created, **kwargs):
    update_avg_rating(instance.reviewee)

@receiver(post_delete, sender=Review)
def update_avg_rating_on_delete(sender, instance, **kwargs):
    update_avg_rating(instance.reviewee)
