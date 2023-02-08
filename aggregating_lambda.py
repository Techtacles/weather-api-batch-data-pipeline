import json
import boto3
import os
sqs_client=boto3.client('sqs')
def aggregate_messages():
    messages=[]
    try:
        resp = sqs_client.receive_message(
            QueueUrl=os.environ.get('SNS_URL'),
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )
        for i in resp['Messages']:
            messages.append(i['MessageId'])
    except KeyError:
        print('No messages on the queue!')
        messages = []
    return f'The total messages the queue has received is {len(messages)}'

def lambda_handler(event, context):
    # TODO implement
    print(event)
    aggregate_messages()
