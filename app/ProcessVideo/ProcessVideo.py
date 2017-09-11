import boto3
import json
import os
import sys
import time
import random

def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])

    try:
        collectionId = sns_msg['jobId']
        print str(collectionId)

    except Exception as e:
        print('Failed to create the collection in Amazon Rekognition')
        print(e)
        raise(e)
