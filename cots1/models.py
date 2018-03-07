from django.db import models

# Create your models here.
class Client(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    displayName = models.CharField(max_length=40)
    secret = models.TextField(default='')
    def __str__(self):
        return self.username
class Token(models.Model):
    username = models.CharField(max_length=40)
    token = models.TextField()
    def __str__(self):
        return self.username
