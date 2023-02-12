from django.db import models
from django.db.models import Model
# Create your models here.
  
class uploadfile(Model):
    file_field = models.FileField()
