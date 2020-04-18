from builtins import Exception

__author__ = "Daksh Patel"

from flask import *
from flask_cors import CORS

from project import app
from project.model.LoginModel import Login
from utils import *

CORS(app)

@app.route('/getUserDetails', methods=['GET', 'POST'])
def getUserCreds():
    login = Login()
    username = request.args.get('username')
    print(username)
    resp = login.getUserDetails(username)
    try:
        name = resp.get('Items')[0].get('name')
        email = resp.get('Items')[0].get('email')
        code = 200
        status = True
        message = 'User details fetched successfully!'
        result = {
            'name': name,
            'email': email,
        }
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result)
    except Exception as e:
        code = 400
        status = False
        message = e.__str__()
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result)
    print(resp)
    return resp
