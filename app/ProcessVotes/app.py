import json
import boto3
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError

app = Chalice(app_name='ProcessVotes')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE_NAME = "FRAC_Votes"

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

@app.route('/CastVote', methods=['POST', 'PUT'], content_types=['application/x-www-form-urlencoded'])
def CastVote():
    request = app.current_request
    stagedvote = request.raw_body


    print request

    identity = request.context['identity']

    # Put the vote into the dynamodb table: TABLE_NAME
    try:
        vote_table = dynamodb.Table(TABLE_NAME)
        resp = vote_table.update_item(
            Key={
                'VoteKey': str(hash("test_key")),
                'VideoID': "Test_video"
            },
            UpdateExpression="set vote = :v",
            ExpressionAttributeValues={
                ':v': str(stagedvote)
            }
        )
        print "Item updated: "
        print json.dumps(resp, indent=4)
        pass
    except Exception as e:
        print "Exception adding item to dynamodb: " + str(e)
        raise

    return str(stagedvote)

@app.route('/GetVotes', methods=['GET'])
def GetVotes():
    request = app.current_request

    return request.to_dict()
