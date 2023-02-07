import json
import os
import boto3
def lambda_handler(event, context):
    # TODO implement
    dynamo_resource=boto3.resource('dynamodb')
    s3=boto3.client('s3',aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('SECRET_KEY'),region_name='us-east-1')
    job_table=dynamo_resource.Table('weather-dynamodb-table')
    
    for obj in event['Records']:
        cleaned_file=obj['s3']['object']['key'].replace('%2C',',').replace('%3A',':')
        print(f'The key is {cleaned_file}')
        csvfile = s3.get_object(Bucket='weather-api-transformed-s3', Key=cleaned_file)
        newfile=csvfile['Body'].read().decode('utf8').split(',')
        json_dump={'psf':str(newfile[-1]),'cloud':newfile[0],'condition':newfile[1],'country':newfile[2],
        'humidity':newfile[3],'last_updated_time':newfile[4],'latitude':newfile[5],'local_time':newfile[6],
        'longitude':newfile[7],'name':newfile[8],'precip_mm':newfile[9],'pressure_mb':newfile[10],'region':newfile[11],
        'temp_c':newfile[12],'wind_dir':newfile[13],'wind_mph':newfile[14]}
        job_table.put_item(Item=json_dump)
        print('Successfully pushed to dynamodb')