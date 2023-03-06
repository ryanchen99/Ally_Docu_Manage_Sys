from django.db.models import Q, Count, Subquery
from django.shortcuts import get_object_or_404
import sys

sys.path.append('../')
# from app import models
from app.models import Clients, Driver_Licenses
from app import models

def client_exists(fname, lname, email, phone):
    # Filter the clients based on the given values
    clients = Clients.objects.filter(
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
    )
    
    # Return True if at least one matching client was found, False otherwise
    return clients.exists()


def driver_license_exist(client_id):
    client = get_object_or_404(Clients, client_id=client_id)
    driver_license = Driver_Licenses.objects.filter(client_id=client.client_id).first()
    if driver_license:
        return True
    else:
        print("Driver license does not exist")
        return False



def create_driver_license(license_number, fname, lname, state, expired_date, issued_date, dob, license_class, image_url, client_id):
    try:
        client = Clients.objects.get(pk=client_id)
    except Clients.DoesNotExist:

        raise ValueError(f"Client with id {client_id} does not exist")

    driver_license = Driver_Licenses.objects.create(
        license_number=license_number,
        fname=fname,
        lname=lname,
        state=state,
        expired_date=expired_date,
        issued_date=issued_date,
        dob=dob,
        license_class=license_class,
        image_url=image_url,
        client_id=client
    )

    return driver_license



def create_client(fname, lname, email, phone):
    # Create a new client
    client = Clients.objects.create(
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
    )
    
    # Return the client object
    return client


