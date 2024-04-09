from django.db import models

# Create your models here.
class marcas(models.Model):
    id_marca = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)