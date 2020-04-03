__author__ = "Daksh Patel"
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


if __name__ == '__main__':
    table = dynamodb.Table('locations')
    table_response = table.scan()
    item_list = table_response['Items']
    # locations = [item['location'] for item in item_list]
    print(item_list)
    table = dynamodb.Table('users')
    # table_response = table.scan()

    name = "Amogh"
    username = "amogh123"
    password = "amogh123"
    phone = "3652287399"
    email = "am210633@dal.ca"

    # response = table.get_item(
    #     Key={
    #         'name': name
    #     }
    # )
    # table = dynamodb_resource.Table(table_name)

    # if filter_key and filter_value:
    filtering_exp = Key('email').eq("dbp2298@gmail.com")
    response = table.scan(FilterExpression=filtering_exp)
    # filtering_exp = Key('email').eq("dbp2298@gmail.com")
    # response = table.query(KeyConditionExpression=filtering_exp)
    # else:
    #     response = table.query()
    # response=table.query(
    #     KeyConditionExpression=Key('email').eq('dbp2298@gmail.com')
    # )
    for i in response[u'Items']:
        print(json.dumps(i, cls=DecimalEncoder))
    # print(response)
    # item = response['Item']
    # print("GetItem succeeded:")
    # print(json.dumps(item, indent=4, cls=DecimalEncoder))
    # print(table)
    # item_list = table.get_item(Key={'loca'})
    # for item in item_list:
    #     item.pop('id', None)
    #     item.pop('location', None)
    # print(item_list)
