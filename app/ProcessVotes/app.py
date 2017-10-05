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


@app.route('/CastVote', methods=['POST'])
def CastVote():
    request = app.current_request
#    print json.dumps(request.headers)
#    print json.dumps(request.query_params)
#    print json.dumps(request.raw_body)
    jsonbody = json.loads(request.raw_body)
#   print json.dumps(request.context)
#    print jsonbody['CognitoID']

    # Set the vote variables from the incoming request
    VoterID = jsonbody['CognitoID']
    VideoID = jsonbody['VideoID']
    Vote = jsonbody['Vote']

    # Put the vote into the dynamodb table: TABLE_NAME
    try:
        vote_table = dynamodb.Table(VOTE_TABLE_NAME)
        DB_resp = vote_table.update_item(
            Key={
                'VideoID': str(VideoID),
                'VoterID': str(VoterID)
            },
            UpdateExpression="set Vote = :v",
            ExpressionAttributeValues={
                ':v': str(Vote),
            }
        )
        print "Item updated: "
        print json.dumps(DB_resp)
        pass
    except Exception as e:
        print "Exception adding item to dynamodb: " + str(e)
        raise

    # Generate the vote total and cache in "totals/<VideoID>.json" on S3 bucket.
    try:
        response = UpdateCachedTotals(VideoID)
        pass
    except Exception as e:
        print "Exception updating vote totals: " + str(e)
        raise

    return response[VideoID]

@app.route('/GetVotes/{VideoID}', methods=['GET'])
def GetVotes(VideoID):
    try:
        vote_table = dynamodb.Table(VOTE_TABLE_NAME)

        query_resp = vote_table.query(
            KeyConditionExpression=Key('VideoID').eq(str(VideoID))
            )
        pass
    except Exception as e:
        print "Exception reading dynamodb: " + str(e)
        raise

    return query_resp['Items']

@app.route('/GetVoteTotals/{VideoID}', methods=['GET'])
def GetVoteTotals(VideoID):
    VoteTotals = {
        str(VideoID): {
            "VideoTitle": "",
            "Votes": {
                "safe": 0,
                "unclear": 0,
                "out": 0,
            }
        }
    }

    try:
        RawVotes = GetVotes(VideoID)
        VideoInfo = GetVideoInfo(VideoID)
        # Set the VideoTitle
        VideoTitle = str(VideoInfo[0]['InputFile']).split('input/',)[1]
        VoteTotals[VideoID]['VideoTitle'] = VideoTitle

        for RawVote in RawVotes:
            VoteTotals[VideoID]['Votes'][str(RawVote['Vote'])] += 1
        print json.dumps(VoteTotals)
        pass
    except Exception as e:
        print "Exception genetating vote totals: " + str(e)
        raise

    return VoteTotals

@app.route('/UpdateCachedTotals/{VideoID}', methods=['GET'])
def UpdateCachedTotals(VideoID):
    # GetVoteTotals for passed VideoID
    CurrentTotals = GetVoteTotals(VideoID)

    # Read in the cached totals from s3
    try:
        S3Object = s3.get_object(Bucket=BUCKET_NAME, Key=VOTES_TOTALS_FILE)
        CachedTotals = json.loads(S3Object['Body'].read().decode('utf-8'))
        print "Existing Totals found on s3"
        print json.dumps(CachedTotals)
        pass
    except Exception as e:
        print "No totals found on s3: " + str(e)
        CachedTotals = {}

    # Update the CachedTotals w/ CurrentTotals for the passed VideoID
    print json.dumps(CurrentTotals[VideoID])
    CachedTotals[VideoID] = CurrentTotals[VideoID]
    print json.dumps(CachedTotals)
    # Update the cached totals on s3
    try:
        response = s3.put_object(Bucket=BUCKET_NAME, Key=VOTES_TOTALS_FILE, Body=json.dumps(CachedTotals))
    except Exception as e:
        print "Error uploading to S3: " + str(e)
        raise

    return CachedTotals

@app.route('/GetVideoInfo/{VideoID}', methods=['GET'])
def GetVideoInfo(VideoID):
    try:
        vote_table = dynamodb.Table(VOD_TABLE_NAME)

        query_resp = vote_table.query(
            KeyConditionExpression=Key('VideoID').eq(str(VideoID))
            )
        pass
        print json.dumps(query_resp)

    except Exception as e:
        print "Exception reading dynamodb: " + str(e)
        raise

    return query_resp['Items']
