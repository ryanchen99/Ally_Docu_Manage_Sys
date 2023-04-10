from django.test import TestCase

# Create your tests here.
import boto3
from botocore.exceptions import ClientError
# from ..backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


# Replace these with your own AWS credentials
AWS_ACCESS_KEY_ID = 'AKIAXHLDP67JDMIB6S44'
AWS_SECRET_ACCESS_KEY = 'jA5GiAgbi5JDRrrm7ybeqGk0mdSwcnE0P6HWK7Xj'
AWS_STORAGE_BUCKET_NAME = 'allyp1bucket'
print("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', "")

print("BUCKET_NAME", AWS_STORAGE_BUCKET_NAME)
def check_bucket_access(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Access to the bucket '{bucket_name}' is permitted.")
        return True
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print(f"Access to the bucket '{bucket_name}' is forbidden.")
        elif error_code == 404:
            print(f"The bucket '{bucket_name}' does not exist.")
        else:
            print(f"An error occurred while accessing the bucket '{bucket_name}': {e}")
        return False

check_bucket_access(AWS_STORAGE_BUCKET_NAME)
