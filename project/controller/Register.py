__author__ = "Daksh Patel"
from flask import *

from project import app
from project.model import dynamodb, DecimalEncoder
from utils import *


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        table = dynamodb.Table('users')
        response = table.put_item(
            Item={
                'username': username,
                'name': name,
                'email': email,
                'password': password
            }
        )
        print(response)
        print(json.dumps(response, indent=4, cls=DecimalEncoder))
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            code = 200
            status = True
            message = 'User details successfully inserted in DynamoDB.'
            result = {}

            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result)
            print(resp)
            return resp
        else:
            code = response['ResponseMetadata']['HTTPStatusCode']
            status = False
            message = 'Something went wrong! Please try again.'
            result = {}
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result)
            print(resp)
            return resp
    else:
        code = 405
        status = False
        message = 'Method not allowed'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result)
        print(resp)
        return resp
