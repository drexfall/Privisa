from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    is_authenticated = models.BooleanField(default=False)

    
class PasswordEntry(models.Model):
    website = models.CharField(max_length=255)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class GeneratorSettings(models.Model):

    digits = models.BooleanField()
    alphabets = models.BooleanField()
    punctuations = models.BooleanField()
    uppercase = models.BooleanField()
    length = models.IntegerField()