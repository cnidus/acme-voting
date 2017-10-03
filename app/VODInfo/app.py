import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from chalice import Chalice
from chalice import NotFoundError
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

app = Chalice(app_name='VODInfo')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE_NAME = "FRAC_VODList_dev"

@app.route('/')
def index():
    request = app.current_request
    print request

    identity = request.context['identity']


    try:
        VOD_table = dynamodb.Table(TABLE_NAME)

        fe = Key('year').between(1950, 1959);
        pe = "#yr, title, info.rating"
        # Expression Attribute Names for Projection Expression only.
        ean = { "#yr": "year", }
        esk = None

        scan_resp = VOD_table.scan(
            #FilterExpression=fe,
            #ProjectionExpression=pe,
            #ExpressionAttributeNames=ean
            )

        # for i in scan_resp['Items']:
        #     print(json.dumps(i, cls=DecimalEncoder))

        # while 'LastEvaluatedKey' in resp:
        #     resp = table.scan(
        #         ProjectionExpression=pe,
        #         FilterExpression=fe,
        #         ExpressionAttributeNames= ean,
        #         ExclusiveStartKey=response['LastEvaluatedKey']
        #         )
        #     for i in resp['Items']:
        #         print(json.dumps(i, cls=DecimalEncoder))
        # pass
    except Exception as e:
        print "Exception reading dynamodb: " + str(e)
        raise

    return json.dumps(scan_resp['Items'], cls=DecimalEncoder)
