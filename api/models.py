from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class AppUser(AbstractUser):
    date_of_birth = models.DateField()

class Hobby(models.Model):
    appUser = models.ManyToManyField(AppUser, through="AppUserDoesHobby")   
    hobby_name = models.CharField(max_length=128)

class AppUserDoesHobby(models.Model):
    hobby_name = models.CharField(max_length=128)
    appUser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)


