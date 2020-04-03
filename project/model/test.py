import decimal
import json

import boto3
from boto3.dynamodb.conditions import Key

from config import *

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region,
)
dynamodb = session.resource('dynamodb',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region, )


def scan_table(table_name, filter_key=None, filter_value=None):
    table = dynamodb.Table(table_name)

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    return response


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


tablename = 'key_destinations'
table = dynamodb.Table(tablename)
response = scan_table(table_name=tablename, filter_key='id', filter_value=None)
print(json.dumps(response['Items'], indent=2, cls=DecimalEncoder))

print()
for item in response['Items']:
    loc = item['location'].lower()
    desc = item['description'].lower()
    name = item['name'].lower()

    response = table.update_item(
        Key={
            'id': item['id'],
        },
        UpdateExpression="set name = :n, location = :l, description = :d,  year = :y",
        ExpressionAttributeValues={
            ':l': loc,
            ':d': desc,
            ':n': name,
            ':y': '1'
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    break
