__author__ = "Amogh Adithya"

import random
import time

from flask import *

from project import app
from project.model import dynamodb
from project.model import scan_table
from utils import *


@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    print('inside make_payment')
    if request.method == 'POST':
        # print(request.form)
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        location = request.form.get('location')
        place = request.form.get('place')
        numTickets = request.form.get('numTickets')
        amount = request.form.get('amount')
        date = request.form.get('date')
        uid = random.randint(1, 1000000)
        table = dynamodb.Table('bookings')
        print(request.form)
        items = {
            'id': uid,
            'user_id': user_id,
            'username': username,
            'ticket_location': place,
            'ticket_city': location,
            'numTickets': numTickets,
            'amount_ticket': amount,
            'date_ticket': date
        }
        generateQRCode(json.dumps(items))
        date_img = time.time()
        uploadImgS3(username, date_img)
        img_url = getUrlQRCode(username, date_img)
        items['img_url'] = img_url
        print(items)
        response = table.put_item(
            Item=items
        )
        # print(response)
        # print(json.dumps(response, indent=4, cls=DecimalEncoder))
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            code = 200
            status = True
            message = 'Booking inserted successfully!'
            result = {
                'uid': uid,
                'img_url': img_url
            }
            print(result)
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result
            )
            print('here', resp)
            return resp
        else:
            code = response['ResponseMetadata']['HTTPStatusCode']
            status = False
            message = 'Something went wrong!'
            result = {}
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result
            )
            print('here', resp)
            return resp
    else:
        code = 405
        status = False
        message = 'Method not allowed!'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        return resp


@app.route('/get_image_url', methods=['GET', 'POST'])
def getImageUrl():
    user_id = request.args.get('user_id')
    response = scan_table(table_name='bookings', filter_key='user_id', filter_value=user_id)
    print(response)
    img_url=response.get('Items')[0].get('img_url')
    code = 200
    status = True
    message = 'Image fetched successfully!'
    result = {
        'img_url': img_url
    }
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result
    )
    return resp

@app.route('/get_my_bookings', methods=['GET', 'POST'])
def getMyBookings():
    user_id = request.args.get('user_id')
    response = scan_table(table_name='bookings', filter_key='user_id', filter_value=user_id)
    items=response['Items']
    for item in items:
        item['id']=int(item['id'])
    finalItems=createNested(items)
    code = 200
    status = True
    message = 'Bookings fetched Successful!'
    result = finalItems
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result
    )
    return resp