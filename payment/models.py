from django.db import models

# Create your models here.

class PayementMode(models.Model):
    title=models.CharField(max_length=30,primary_key=True)
    description = models.CharField(max_length=1000)
