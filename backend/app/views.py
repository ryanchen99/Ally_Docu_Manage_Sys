from django.shortcuts import render, HttpResponse
from app import models
# Create your views here.
def home(request):
    return HttpResponse("Hello World")


def create_client(request):
    from app.utils.crud import create_client
    client = create_client('Zixin', 'Li',"9999@email.edu", "0020201")
    print(client)
    return HttpResponse("Client created")

def client_exists(request):
    from app.utils.crud import client_exists
    # IMPORTANT: client_exists() takes either only one parameter (client_id) 
    # or four parameters (fname, lname, email, phone).
    exists = client_exists(id = 2)
    if exists:
        return HttpResponse("Client exist")
    return HttpResponse("Client does not exist")


def create_driver_license(request):
    from app.utils.crud import create_driver_license
    driver_license = create_driver_license('00001', 'Zixin', 'Li', 'CA', '2021-12-31', '2021-01-01', '2000-01-01', 'A', 'images/', 21)
    print(driver_license)
    return HttpResponse("Driver license created")


def document_exist(request):
    from app.utils.crud import document_exist
    from django.http import Http404
    try:
        exists = document_exist(1, "Driver's License")
    except Http404:
        return HttpResponse("Client does not exist")
    except ValueError as e:
        return HttpResponse(e)
    print(type(exists))
    if exists:
        return HttpResponse("Driver license exist")
    return HttpResponse("Driver license does not exist")
    # return HttpResponse("hi")