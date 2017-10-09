import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError

app = Chalice(app_name='VODInfo')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE_NAME = "FRAC_VODList_dev"

@app.route('/GetVODList', methods=['GET'], cors=True)
def GetVODList():
    formatted = []
    request = app.current_request

    try:
        VOD_table = dynamodb.Table(TABLE_NAME)
        scan_resp = VOD_table.scan()

    except Exception as e:
        print "Exception reading dynamodb: " + str(e)
        raise

    for item in scan_resp['Items']:
        formatted.append({
            "VideoID": item['VideoID'],
            "FileName": str(item['InputFile']).split('input/')[1],
            "Outputs": json.loads(item['outputs']),
            })

    return formatted
