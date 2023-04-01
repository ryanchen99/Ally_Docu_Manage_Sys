from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from app.models import *
import json

from app.utils.crud import DOCUMENT_TYPE_MAPPING, get_client_documents,get_true_docu_attributes
# Create your views here.

@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        id = data.get('id', None)
        print(id)
        if id is not None:
            from app.utils.crud import create_client
            client = create_client(id)
            print(client)
            return HttpResponse("Client created")
        else:
            return JsonResponse({'error': 'docu_type not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def client_documents(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        client_id = data.get('id', None)
        print(client_id)
        client_documents = get_true_docu_attributes(client_id)
        if client_documents:
            print(client_documents, type(client_documents))
            data = {
                "client_id": client_id,
                "documents": client_documents
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({'error': 'Client not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def driver_license_handler(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        docu_type = data.get('docu_type', None)
        print(docu_type)
        if docu_type is not None:
            document = DOCUMENT_TYPE_MAPPING[docu_type].objects.all()
            serialized_data = serializers.serialize('json', document)
            print(document)
            return JsonResponse(serialized_data, safe=False)
        else:
            return JsonResponse({'error': 'docu_type not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def client_exists(request):
    from app.utils.crud import client_exists
    # IMPORTANT: client_exists() takes either only one parameter (client_id) 
    # or four parameters (fname, lname, email, phone).
    exists = client_exists(id = 2)
    
    if exists:
        return HttpResponse("Client exist")
    return HttpResponse("Client does not exist")

@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        # Get the file from the request
        uploaded_file = request.FILES.get('file')
        print(uploaded_file, type(uploaded_file))

        if uploaded_file is not None:
            # Process the file (e.g., save it to disk, analyze it, etc.)
            # This example just prints the file name and size
            print(f'File name: {uploaded_file.name}, File size: {uploaded_file.size} bytes')

            # Return a JSON response with some information
            response_data = {'info': 'File uploaded successfully'}
            return JsonResponse(response_data)
        else:
            response_data = {'error': 'No file was provided'}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=405)

def create_driver_license(request):
    from app.utils.crud import create_driver_license
    driver_license = create_driver_license('00001', 'Zixin', 'Li', 'CA', '2021-12-31', '2021-01-01', '2000-01-01', 'A', 'images/', 1)
    print(driver_license)
    return HttpResponse("Driver license created")

@csrf_exempt
def document_exist(request):
    if request.method == 'GET':
        return HttpResponse("hi")
    print("------------------",request.headers)
    from app.utils.crud import document_exist, client_exists
    from django.http import Http404
    try:
        # Decode the request body as JSON
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    if "id" in data:
        id = data['id']
    else:
        fname, lname, email, phone = data['fname'], data['lname'], data['email'], data['phone']
        id = client_exists(fname, lname, email, phone)
    if not id:
        return JsonResponse({'Status': -1})
    document = data["document"]
    try:
        exists = document_exist(id, document)
    except Http404:
        return JsonResponse({'Status': 0})
    except ValueError as e:
        return JsonResponse({'Status': -2})
    if exists:
        return JsonResponse({'Status': 1})
    return JsonResponse({'Status': 0})
