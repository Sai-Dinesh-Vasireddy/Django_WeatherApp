from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25,default="",unique = True)

    def __str__(self):
        return self.name