#Importing libraries
import requests
import json
import boto3
from datetime import datetime
import os
#Get the base date and time
def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

#Get the response 
def get_response():
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":"Nigeria"}
    headers = {
	"X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response

#Get events in json format
def get_values(response):
    event=json.loads(response.content.decode('utf8'))
    push_event={'name':event['location']['name'],'region':event['location']['name'],
    'country':event['location']['country'],'latitude':event['location']['lat'],
    'longitude':event['location']['lon'],'local_time':event['location']['localtime'],
    'last_updated_time':event['current']['last_updated'],'temp_c':event['current']['temp_c'],
    'condition':event['current']['condition']['text'],'wind_mph':event['current']['wind_mph'],
    'wind_dir':event['current']['wind_dir'],'humidity':event['current']['humidity'],'cloud':event['current']['cloud'],
    'pressure_mb':event['current']['pressure_mb'],'precip_mm':event['current']['precip_mm']}
    return str(push_event)

#Get the s3 client using Boto3's client api
def get_s3_client():
    s3=boto3.client('s3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),region_name='us-east-1')
    return s3

#Upload files to s3
def upload_to_s3(client):
    response=client.put_object(Body=get_values(get_response()),Bucket='weather-api-raw-s3',Key=get_current_datetime())

#Run the ingestion pipeline
def main():
    upload_to_s3(get_s3_client())
    return f'Successfully uploaded {get_values(get_response())}'

def lambda_handler(event, context):
    # TODO implement
    main()
    print(event)

