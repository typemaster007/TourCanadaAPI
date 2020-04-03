__author__ = "Daksh Patel"
import os

import boto3
import pyqrcode
from botocore.exceptions import NoCredentialsError
from flask import jsonify
import base64
import requests
s3 = boto3.client('s3')


def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def capitalizeAll(object):
    if type(object) == dict:
        keys = object.keys()
        for key in keys:
            if type(object[key]) == str:
                if object[key].startswith('http'):
                    continue
                object[key] = object[key].title()
            elif type(object[key]) == list:
                object[key] = capitalizeAll(object[key])
            else:
                pass
    elif type(object) == list:
        for i in range(len(object)):
            if type(object[i]) == dict:
                object[i] = capitalizeAll(object[i])
            elif type(object[i]) == str:
                if object[i].startswith('http'):
                    continue
                object[i] = object[i].title()
            else:
                pass
    else:
        pass
    return object


def encryptEmail(email):
    li = email.split('@')
    handle = li[0][:2] + '*' * (len(li[0]) - 2)
    domain = li[1].split('.')
    dom = domain[0][:2] + '*' * (len(domain[0]) - 2)
    ain = domain[1][:1] + '*' * (len(domain[1]) - 1)
    final_email = '{}@{}.{}'.format(handle, dom, ain)
    return final_email


def createNested(obj):
    finalTrends = []
    temp = []
    for i in range(len(obj)):
        # print(i)
        if (i % 3 == 0 and i != 0):
            finalTrends.append(temp)
            temp = []
        temp.append(obj[i])
        if i == len(obj) - 1:
            finalTrends.append(temp)
            temp = []
    return finalTrends


def createResponse(status_value, code, message, result={}):
    resp = {
        'status': status_value,
        'code': code,
        'message': message,
        'result': result
    }
    resp = jsonify(resp)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


def generateQRCode(data):
    data = pyqrcode.create(data)
    data.png('qrcodes/temp.png', scale=3)


def uploadImgS3(username, date):
    filename = 'qrcodes/temp.png'
    bucket = "www.tourcanada.ca"
    print(date)
    # date = date.split('-')
    # date = '_'.join(date)
    s3filename = "users/{}/ticket_{}.png".format(username, date)
    upload_to_aws(filename, bucket, s3filename)
    os.remove(filename)

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def getUrlQRCode(username, date):
    # date = date.split('-')
    # date = '_'.join(date)
    s3filename = "users/{}/ticket_{}.png".format(username, date)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'www.tourcanada.ca',
            'Key': s3filename
        }
    )
    start="data:image/png;base64,"
    url=start+get_as_base64(url).decode()
    print('url',url)
    return url

if __name__ == '__main__':
    import json

    obj = [
        {
            1: 'ferfr sdfd',
            2: ['wewe,aas', 'wewe,aas']
        },
        {
            1: 'ferfr sdfd',
            2: 'wewe,aas',
            3: 3
        }

    ]
    generateQRCode(json.dumps(obj))
