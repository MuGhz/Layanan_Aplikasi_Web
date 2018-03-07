from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=40)
    displayName = models.CharField(max_length=40)
    def __str__(self):
        return self.username
