from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class attend(models.Model):
    Fname = models.CharField(max_length=16)
    Lname = models.CharField(max_length=16)
    Status = models.BooleanField(null=True)
    def __str__(self):
        return self.Fname
    

