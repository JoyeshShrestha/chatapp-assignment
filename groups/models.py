from django.db import models
from user_profile.models import User
# Create your models here.
class Groups(models.Model):
    name = models.CharField(max_length=255, unique = True)
    members = models.ManyToManyField(User, related_name='group', null= True)

    def __str__(self):
        return self.name