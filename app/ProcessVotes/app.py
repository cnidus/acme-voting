import json
import boto3
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError

app = Chalice(app_name='ProcessVotes')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

@app.route('/CastVote', methods=['POST', 'PUT'])
def CastVote():
    request = app.current_request
    if request.method == 'PUT':
        stagedvotes[key] == request.json_body
    elif request.method == 'POST':
        stagedvotes[key] == request.json_body

    identity = request.context['identity']

    #Create the dynamodb table
    try:
        table_vote = dynamodb.create_table(
            TableName='FRAC_Votes',
            KeySchema=[
                {
                    'AttributeName': 'VoteKey',
                    'KeyType': 'HASH'    #Partition Key
                },
                {
                    'AttributeName': 'VideoID',
                    'KeyType': 'RANGE'    #Sort Key for the video that's being voted on.
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'VoteKey',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'VideoID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'VoterID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Vote',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print "FRAC_Votes dynamodb table created"
        pass
    except Exception as e:
        
        raise

    return json.dumps(identity)

@app.route('/GetVotes', methods=['GET'])
def GetVotes():
    request = app.current_request

    return request.to_dict()
