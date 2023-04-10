from django.db.models import Q, Count, Subquery
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

import sys

sys.path.append('../')
# from app import models
from app.models import *
from app import models

DOCUMENT_TYPE_MAPPING = {
    "Armed Forces of the U.S. ID Card (front and back)":0,
    "Birth Certificate":1,
    "Copy of Death Certificate":2,
    "Death Notification Entry - Federal Government":3,
    "Divorce Decree":Divorce_Decrees,
    "Driver's License":Driver_Licenses,
    "Executor Documents (For an estate, but not an IRA)":6,
    "Google Maps/USPS Address Search":7,
    "Latest, best data provided by customer":8,
    "Legal Name Change Document":9,
    "LexisNexis":10,
    "LexisNexis - For minor spelling corrections":11,
    "Marriage Certificate":12,
    "Medicare Card":13,
    "Notice of Reclamation - Federal Government":14,
    "Obituary":15,
    "Original Death Certificate":16,
    "Permanent Resident Card":17,
    "Signed Social Security Card":18,
    "Signed SSN Card w/new name":19,
    "State Issued ID":20,
    "U.S. Military Card":21,
    "U.S. Passport Card":22,
    "W-2":23,
    "W-9":24,
}

class Document_Type:
    MAGIC_NUMBER = 42
    MAX_ATTEMPTS = 3
    TIMEOUT_SECONDS = 30


def client_exists(fname, lname, email, phone):
    clients = Clients.objects.filter(
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
    )
    # print(clients)
    if clients:
        return clients.first().client_id
    else:
        return None


def document_exist(client_id, document_type):
    # client = get_object_or_404(Clients, client_id=client_id)
    
    if document_type in DOCUMENT_TYPE_MAPPING:
        document_type = DOCUMENT_TYPE_MAPPING[document_type]
    else:
        print(f"Document type {document_type} does not exist")
        raise ValueError(f"Document type {document_type} does not exist")
    
    try:
        document = document_type.objects.get(client_id=client_id)
    except document_type.DoesNotExist:
        document = None

    if document:
        return True
    print(f"Document type {document_type} does not exist")
    return False

def create_a_client(id,fname, lname, email, phone):
    client = Clients(
        client_id=id,
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
    )
    client.save()
    return client

def get_true_docu_attributes(client_id):
    try:
        # Fetch the Docu_of_Clients instance for the given client_id
        docu_of_client = Docu_of_Clients.objects.get(client_id=client_id)
        # Iterate over the fields and store the field names with a value of True
        true_attributes = []
        for field in docu_of_client._meta.fields:
            if field.name != 'client_id' and getattr(docu_of_client, field.name):
                true_attributes.append(field.name)
        # print(true_attributes)
        return true_attributes

    except ObjectDoesNotExist:
        return None


def get_client_documents(client_id):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        client_documents = Docu_of_Clients.objects.get(client_id=client_id)
        return client_documents
    except ObjectDoesNotExist:
        return None
    

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



def create_client(id):
    # Create a new Docu_of_Clients instance with the new client's ID and save it
    new_docu_of_client = Docu_of_Clients(client_id=id)
    new_docu_of_client.save()

    return new_docu_of_client


