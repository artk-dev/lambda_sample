import json
import boto3
import uuid
from urllib.parse import unquote_plus
import xml.etree.ElementTree as ET

def lambda_handler(event, context):
    s3 = boto3.resource('s3', region_name='eu-west-2')

    #Loops through every file uploaded
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        bucket = s3.Bucket(bucket_name)
        key = unquote_plus(record['s3']['object']['key'])

        # Temporarily download the xml file for processing
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        bucket.download_file( key, download_path)

        machine_id = get_machine_id_from_file(download_path)

        bucket.upload_file(download_path, machine_id+'/'+key[9:])
        
        s3.Object(bucket_name,key).delete()

def get_machine_id_from_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    return root[0].text