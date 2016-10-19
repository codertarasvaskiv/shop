from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_logo = models.ImageField(upload_to='user_images', blank=True)

    def __str__(self):
        return self.name*5


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    color = models.CharField(max_length=20)
    style = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    usage = models.CharField(max_length=20)
    sport = models.IntegerField()
    brand = models.CharField(max_length=20)
    product_logo = models.ImageField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name + ' ' + str(self.price)