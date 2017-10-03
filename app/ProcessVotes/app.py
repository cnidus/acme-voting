import json
import boto3
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from botocore.client import Config

app = Chalice(app_name='ProcessVotes')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

VOTE_TABLE_NAME = "FRAC_Votes_dev2"
VOD_TABLE_NAME = "FRAC_VODList_dev"
BUCKET_NAME = "frac-voting"
VOTES_TOTALS_FILE = "votetotals.json"

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

    # Set the vote variables from the incoming request
    VoterID = "test_identity"
    VideoID = "1506992170643-ej4cw8"
    Vote = str(stagedvote)

    # Put the vote into the dynamodb table: TABLE_NAME
    try:
        vote_table = dynamodb.Table(VOTE_TABLE_NAME)
        resp = vote_table.update_item(
            Key={
                'VideoID': str(VideoID),
                'VoterID': str(VoterID)
            },
            UpdateExpression="set Vote = :v, VoterID = :i",
            ExpressionAttributeValues={
                ':v': str(Vote),
            }
        )
        print "Item updated: "
        print json.dumps(resp, indent=4)
        pass
    except Exception as e:
        print "Exception adding item to dynamodb: " + str(e)
        raise

    # Generate the vote total and cache in "totals/<VideoID>.json" on S3 bucket.
    try:
        # Read in the cached totals from s3
        # VoteTotals =
        # Calculate totals for VideoID
        # VoteTotalsGetVoteTotals()
        # Update the cached totals on s3
        pass
    except Exception as e:
        print "Exception genetating vote totals: " + str(e)
        raise


    return str(stagedvote)

@app.route('/GetVotes/{VideoID}', methods=['GET'])
def GetVotes(VideoID):
    # request = app.current_request
    # stagedvote = request.raw_body
    print str(VideoID)

    try:
        vote_table = dynamodb.Table(VOTE_TABLE_NAME)

        query_resp = vote_table.query(
            KeyConditionExpression=Key('VideoID').eq(str(VideoID))
            )

        pass
        # print json.dumps(query_resp)

    except Exception as e:
        print "Exception reading dynamodb: " + str(e)
        raise

    return query_resp['Items']

@app.route('/GetVoteTotals/{VideoID}', methods=['GET'])
def GetVoteTotals(VideoID):
    VoteTotals = {
        "safe": 0,
        "unclear": 0,
        "out": 0,
    }

    try:
        RawVotes = GetVotes(VideoID)
        for RawVote in RawVotes:
            VoteTotals[str(RawVote['Vote'])] += 1
        print json.dumps(VoteTotals)
        pass
    except Exception as e:
        print "Exception genetating vote totals: " + str(e)
        raise

    return VoteTotals
