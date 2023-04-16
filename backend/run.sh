#!/bin/bash

export AWS_STORAGE_BUCKET_NAME='allyp1bucket'
export AWS_S3_REGION_NAME='us-east-1'
export DATABASE_ENGINE='django.db.backends.postgresql'
export DATABASE_NAME='postgres'
export DATABASE_USER='postgres'
export DATABASE_PASSWORD="postgres"
export DATABASE_HOST='database-1.cehuiblb6pba.us-east-1.rds.amazonaws.com'
export DATABASE_PORT='5432'
export DEBUG=TRUE
export DJANGO_ALLOWED_HOSTS="44.204.83.244,localhost,127.0.0.1"

# python3 manage.py check
# python3 manage.py makemigrations app
# python3 manage.py migrate app
python3 manage.py runserver