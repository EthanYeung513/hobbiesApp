from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class Hobby(models.Model):
    hobby_name = models.CharField(max_length=128)

class AppUser(AbstractUser):
    date_of_birth = models.DateField()
    hobbies = models.ManyToManyField(Hobby, through='AppUserHobby')
    REQUIRED_FIELDS = ['date_of_birth'] #for superuser prompt


class AppUserHobby(models.Model):
    appUser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    date_started = models.DateField()
    level_of_expertise = models.CharField(max_length=128)


