from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from app.models import *
import json
import boto3
from app.utils.ocr import parse_CA_DL
from app.utils.crud import DOCUMENT_TYPE_MAPPING, get_client_documents,get_true_docu_attributes
# Create your views here.


# create client info for docu_of_client table, so that we can track which documents are uploaded for this client
@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        id = data.get('id', None)
        print(id)
        if id is not None:
            from app.utils.crud import create_client
            client = create_client(id)
            print(client, "Docu_of_Clients has been created")
            return HttpResponse("Docu_of_Clients for this clients created")
        else:
            return JsonResponse({'error': 'docu_type not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_a_client(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        id = data.get('id', None)
        fname = data.get('fname', None)
        lname = data.get('lname', None)
        email = data.get('email', None)
        phone = data.get('phone', None)
        print(id)
        if id is not None:
            from app.utils.crud import create_a_client
            client = create_a_client(id, fname, lname, email, phone)
            print(client, "Client has been created")
            return HttpResponse("Client created")
        else:
            return JsonResponse({'error': 'docu_type not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# check what documents exist for a client with the given client_id
@csrf_exempt
def client_documents(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        client_id = data.get('id', None)
        print(client_id)
        client_documents = get_true_docu_attributes(client_id)
        # print(client_documents, type(client_documents))
        if client_documents is not None:
            print(client_documents, type(client_documents))
            data = {
                "documents": client_documents
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({'error': 'Client not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
# show all driver license in database
@csrf_exempt
def show_all_dl(request):
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
        # print(data)
        # request_data = json.loads(request.body)
        uploaded_file = request.FILES.get('file', None)
        client_id = request.POST.get('user', None)

        print("1111",uploaded_file, type(uploaded_file))
        print("1111",client_id, type(client_id))

        if uploaded_file is not None:
            # Process the file (e.g., save it to disk, analyze it, etc.)
            # This example just prints the file name and size
            # print(f'File name: {uploaded_file.name}, File size: {uploaded_file.size} bytes')
            parsed_info = parse_CA_DL(uploaded_file.name, uploaded_file)
            print(parsed_info)
            # Upload the file to S3
            s3 = boto3.client('s3')
            bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', "")
            print("bucket_name", bucket_name)
            extension = uploaded_file.name.split(".")[-1]
            print(client_id, "client_id", extension, "extension")
            file_name = client_id+'_'+"driver_license."+extension
            uploaded_file.name = file_name
            print("uploaded_file.name", uploaded_file.name)
            s3_key = f'documents/{uploaded_file.name}'
            s3.upload_fileobj(uploaded_file, bucket_name, s3_key)

            # Generate a presigned URL to access the file
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': s3_key},
                ExpiresIn=3600  # URL expires in 1 hour
            )
            print(url)
            # Return a JSON response with some information
            response_data = {"info": parsed_info, "document_url": url}
            # print(response_data)
            return JsonResponse(response_data)
        else:
            response_data = {'error': 'No file was provided'}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=405)
    
@csrf_exempt
def confirm_document(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('client_id')
        docu = data.get('docu')
        url = data.get('document_url')
        # print(url, type(url), len(url))

        from datetime import datetime
        # Parse date fields
        dob = datetime.strptime(docu.get('Date_of_Birth (MM/DD/YYYY)'), '%m/%d/%Y') if docu.get('Date_of_Birth (MM/DD/YYYY)') else None
        issued_date = datetime.strptime(docu.get('Issue_Date (MM/DD/YYYY)'), '%m/%d/%Y') if docu.get('Issue_Date (MM/DD/YYYY)') else None
        expired_date = datetime.strptime(docu.get('Expiration_Date (MM/DD/YYYY)'), '%m/%d/%Y') if docu.get('Expiration_Date (MM/DD/YYYY)') else None

        # Check if client_id exists in the DriverLicense table
        existing_entries = Driver_Licenses.objects.filter(client_id=client_id)
        client = Clients.objects.get(client_id=client_id)

        # If there are existing entries, delete them
        if existing_entries.exists():
            existing_entries.delete()

        # Create a new Driver_Licenses object
        driver_license = Driver_Licenses(
            license_number=docu.get('License_Number') or '',
            fname=docu.get('First_Name') or '',
            lname=docu.get('Last_Name') or '',
            sex=docu.get('SEX') or '',
            address=docu.get('Address') or '',
            city=docu.get('City') or '',
            state=docu.get('State') or '',
            zip=docu.get('Zip') or '',
            expired_date=expired_date,
            issued_date=issued_date,
            dob=dob,
            image_url=url,
            license_class=docu.get('Class') or '',
            client_id=client,
        )
        # Save the object to the database
        driver_license.save()
        # print("=======================================")

        doc = Docu_of_Clients.objects.get(client_id=client_id)
        doc.drivers_license = True
        doc.save()
        # print("====================+++++++++++++++++===================")
        return JsonResponse({"message": "Driver License created successfully."}, status=201)

    return JsonResponse({"error": "Invalid request method."}, status=405)


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
