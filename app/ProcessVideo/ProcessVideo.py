import boto3
import json
import os
import sys
import time
import random

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE_NAME = "FRAC_VODList_dev"

def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])

    videoId = sns_msg['jobId']
    inputFileName = sns_msg['input']['key']
    outputs = sns_msg['outputs']


    #Try to update dynamodb w/ the files
    if str(sns_msg['state']) == 'COMPLETED':
        #ETS status == completed, so lets proceed
        try:
            good_outputs = []
            bad_outputs = []
            for out in outputs:
                if str(out['status']) == 'Complete':
                    good_outputs.append(out)
                else:
                    bad_outputs.append(out)

            #Only send the completed outputs to DynamoDB
            if len(good_outputs) >= 1:
                video_table = dynamodb.Table(TABLE_NAME)
                resp = video_table.update_item(
                    Key={
                        'VideoID': str(videoId),
                    },
                    UpdateExpression="set outputs = :o, InputFile = :i",
                    ExpressionAttributeValues={
                        ':o': json.dumps(good_outputs),
                        ':i': str(inputFileName)
                    }
                )
                print "Item updated: "
                print json.dumps(resp)
            else:
                print "No Successful outputs found for video: " + str(videoId)
            pass

        except Exception as e:
            print('Failed to update DynamoDB')
            print(e)
            raise(e)
    else:
        #The job didnt complete successfully, write a message.
        print "ElasticTranscoder job did not complete, with status: " + str(sns_msg['state'])
