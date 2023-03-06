from django.db import models

# Create your models here.
class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    
class Driver_Licenses(models.Model):
    dl_id = models.AutoField(primary_key=True)
    license_number = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    expired_date = models.DateField()
    issued_date = models.DateField()
    dob = models.DateField()
    license_class = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/')
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)

