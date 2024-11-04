from django.db import models
from django.contrib.auth.models import User

JOURNEY_STATUS = (
    (0, 'Pending'),
    (1, 'Active'),
    (2, 'Completed'),
    (3, 'Cancelled'),
)

MEETING_STATUS = (
    (0, 'Proposed'),
    (1, 'Accepted'),
    (2, 'Rejected'),
)

REQUEST_STATUS = (
    (0, 'Pending'),
    (1, 'Accepted'),
    (2, 'Rejected'),
    (3, 'Withdrawn'),
)

class Journey(models.Model):
    """
    Using decimals for longitude and latitude rather than point so I don't
    have to install extra packages for Django to deal with spatial stuff.
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    start_location_long = models.DecimalField(max_digits=20, decimal_places=15)
    start_location_lat = models.DecimalField(max_digits=20, decimal_places=15)
    destination_long = models.DecimalField(max_digits=20, decimal_places=15)
    destination_lat = models.DecimalField(max_digits=20, decimal_places=15)
    posted_at = models.DateTimeField(auto_now_add=True)
    cancelled_time = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=JOURNEY_STATUS, default=0)
    
    def __str__(self):
        return self.title + ' by ' + self.creator.userprofile.name

    class Meta:
        ordering = ['-posted_at']
        

class Request(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    request_message = models.CharField(max_length=255)
    withdraw_message = models.CharField(max_length=255, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=REQUEST_STATUS, default=0)
    
    def __str__(self):
        return self.journey.title + ': Request by ' + self.requester.username

    class Meta:
        ordering = ['-created_at']
            

class Meeting(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    meeting_time = models.TimeField()
    meeting_location_long = models.DecimalField(max_digits=20, decimal_places=15)
    meeting_location_lat = models.DecimalField(max_digits=20, decimal_places=15)
    status = models.IntegerField(choices=MEETING_STATUS, default=0)
    
    def __str__(self):
        return self.user.username + ' meeting for ' + self.journey.title

    class Meta:
        ordering = ['-status']
        
    def save(self, *args, **kwargs):
        if self.status == 1:
            other_meetings = Meeting.objects.filter(journey=self.journey).exclude(pk=self.pk)
            for meeting in other_meetings:
                meeting.status = 2
                meeting.save()
        super(Meeting, self).save(*args, **kwargs)
    