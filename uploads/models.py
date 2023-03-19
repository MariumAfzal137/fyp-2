from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Model
# Create your models here.
  
class uploadfile(Model):
    file_field = models.FileField()

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class Dataset(models.Model):
    Id=models.CharField(max_length=255,unique=True)
    UserId=models.ForeignKey(User, on_delete=models.CASCADE)
    File=models.FileField()

class Chart(models.Model):
    LINE = 'Line'
    BAR = 'Bar'
    PIE = 'Pie'
    Id= models.CharField(max_length=255,unique=True)
    UserId= models.ForeignKey(User, on_delete=models.CASCADE)
    DataSetId= models.ForeignKey(Dataset, on_delete=models.CASCADE)
    
    charttype = [
       (BAR, ('Bar Graph')),
       (PIE, ('Pie Chart')),
       (LINE, ('Line Graph')),
   ]
    ChartType=models.CharField(max_length=255,choices=charttype,null=False,default='BAR')
    Svg = models.FileField()

class Report(models.Model):
    Id= models.CharField(max_length=255,unique=True)
    UserId= models.ForeignKey(User, on_delete=models.CASCADE)
    DataSetId= models.ForeignKey(Dataset, on_delete=models.CASCADE)
    ChartId=models.ForeignKey(Chart, on_delete=models.CASCADE)