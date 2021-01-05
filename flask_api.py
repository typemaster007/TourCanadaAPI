__author__ = "Amogh Adithya"

import json
import random

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, request, g

aws_access_key_id = 'AKIA5WTK4BJPARQ7JDBC'
aws_secret_access_key = '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'
region = 'us-east-2'

app = Flask(__name__)


@app.before_request
def before_request():
    g.session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )

    g.dynamodb = g.session.resource('dynamodb',
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key,
                                    region_name=region, )


# get a list of locations
@app.route('/locations/', methods=['GET'])
def get_locations():
    table = g.dynamodb.Table('locations')
    table_response = table.scan()
    item_list = table_response['Items']
    # print(item_list[0]['photoURL'])
    locations = [item['location'] for item in item_list]
    images = [item['photoURL'] for item in item_list]
    return jsonify({'locations': locations, 'images': images})


@app.route('/destinations', methods=['GET'])
def get_destinations():
    location = request.args['location']
    table = g.dynamodb.Table('key_destinations')
    fe = Key('location').eq(location)
    table_response = table.scan(
        FilterExpression=fe
    )
    item_list = table_response['Items']
    for item in item_list:
        item.pop('id', None)
        item.pop('location', None)
    return jsonify({'result': item_list})


@app.route('/bookings', methods=['GET', 'POST'])
def get_bookings():
    if request.method == 'GET':
        user_id = request.args['user']
        table = g.dynamodb.Table('bookings')
        fe = Key('user_id').eq(user_id)
        table_response = table.scan(
            FilterExpression=fe
        )
        item_list = table_response['Items']
        # print(item_list)
        for item in item_list:
            item.pop('id', None)
            item.pop('user_id', None)
        return jsonify({'result': item_list})
    if request.method == 'POST':

        try:
            request_data = json.loads(request.data.decode('UTF-8'))
            user_id = request_data['user']
            location = request_data['location']
            table = g.dynamodb.Table('bookings')
            table.put_item(
                Item={
                    'id': random.randint(1, 1000000),
                    'user_id': user_id,
                    'location': location
                }
            )
            return jsonify({'status': "success"})
        except Exception as e:
            print("exception", e)
            return jsonify({'status': "failed"})


if __name__ == "__main__":
    app.run(debug=True)
