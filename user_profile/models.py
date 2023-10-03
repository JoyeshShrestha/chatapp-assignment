from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =[username,email,password]

    
    