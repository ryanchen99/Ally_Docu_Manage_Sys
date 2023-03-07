from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware import csrf
from app import models
import json
# Create your views here.
def home(request):
    if request.method == "GET":
        # print(csrf.get_token(request))
        return render(request, "home.html")
    # 如果是POST请求，获取用户提交的数据
    # print(request.POST)
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    if username == 'root' and password == "123":
        # return HttpResponse("登录成功")
        return redirect("http://www.google.com")

    # return HttpResponse("登录失败")
    return render(request, 'home.html', {"error_msg": "用户名或密码错误"})


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
    if request.method == 'GET':
        return HttpResponse("hi")
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
