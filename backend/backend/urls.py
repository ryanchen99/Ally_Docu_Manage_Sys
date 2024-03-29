"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('create_client/',views.create_client),
    path('create_driver_license/',views.create_driver_license),
    path('document_exist/',views.document_exist),
    path('client_exists/',views.client_exists),
    path('show_all_dl/',views.show_all_dl),
    path('client_documents/',views.client_documents),
    path('file_upload/',views.file_upload),
    path('confirm_document/',views.confirm_document),
    path('create_a_client/',views.create_a_client),
]
