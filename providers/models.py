from django.db import models



class Provider (models.Model):
    name = models.CharField(max_length=30)
    
