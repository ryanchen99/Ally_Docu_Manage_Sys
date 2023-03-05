from django.shortcuts import render, HttpResponse
from app import models
# Create your views here.
def home(request):
    return HttpResponse("Hello World")

def orm(request):
    models.Clients.objects.create(fname='Ruihan', lname='Chen',email='00@email.edu',phone='0000')
    models.Clients.objects.create(fname='Hao', lname='Tang',email='01@email.edu',phone='111111')

    
    
    
    return HttpResponse("ORM succeed")