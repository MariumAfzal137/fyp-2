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
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    file=models.FileField()

class Chart(models.Model):
    class chartTypes(models.TextChoices):
        BarGraph='Bar'
        LineGraph='Line'
        PieChart='Pie'
        AreaChart='Area'
    user= models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    dataSet= models.ForeignKey(Dataset, on_delete=models.CASCADE)
    title=models.CharField(max_length=20,null=False,default="title unknown")
    chartType=models.CharField(max_length=20,choices=chartTypes.choices,null=False,default='Bar')
    image = models.FileField(upload_to='uploads/Files/',null=True,blank=True)

class Report(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    dataSet= models.ManyToManyField(Dataset)
    chart=models.ManyToManyField(Chart)