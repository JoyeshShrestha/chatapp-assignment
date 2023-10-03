from django.db import models
from user_profile.models import User
from groups.models import Groups
# Create your models here.
class Notifications(models.Model):
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    recipient_group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    has_seen = models.BooleanField(default=False)
    def __str__(self):
        return self.name