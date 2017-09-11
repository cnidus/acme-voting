import json
import boto3
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


try:
    table_vote = dynamodb.create_table(
        TableName='FRAC_VODList_dev',
        KeySchema=[
            {
                'AttributeName': 'VideoID',
                'KeyType': 'HASH'    #Partition Key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'VideoID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
    )
    print "FRAC_VODList dynamodb table created"


    pass
except Exception as e:
    print "Exception creating dynamodb" + str(e)
    raise
