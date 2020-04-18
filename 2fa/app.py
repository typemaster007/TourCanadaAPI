__author__ = 'Daksh Patel'

import datetime
from bson import ObjectId
from flask import *
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_security import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['MONGODB_SETTINGS'] = {
    'db': 'tourcanada',
    'host': '18.207.227.150',
    'port': 27017,
    'username': 'csci5409',
    'password': 'group10',
    'authentication_source': 'admin'
}
app.config['SECURITY_PASSWORD_SALT'] = 'abc'

# Create database connection object
db = MongoEngine(app)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'tourcanada5409@gmail.com',
    "MAIL_PASSWORD": 'cloudgroup10'
}
app.config.update(mail_settings)
mail = Mail(app)


def sendEmail(email, subject='Verification email', sender=app.config.get('MAIL_USERNAME'),
              body="This is the verification email"):
    with app.app_context():
        msg = Message(subject=subject,
                      recipients=[email],
                      html=body,
                      sender=sender,
                      )
        mail.send(msg)

    return "Email sent!"


class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    phone_no = db.StringField(max_length=255)
    username = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=False)
    confirmed_at = db.DateTimeField()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        print(type(ObjectId(data['id'])))
        user = User.objects.get(id=ObjectId(data['id']))
        user.confirmed_at = datetime.datetime.now()
        user.active = True
        user.save()
        return user

def createResponse(status_value, code, message, result=None):
    if result is None:
        result = {}
    resp = {
        'status': status_value,
        'code': code,
        'message': message,
        'result': result,
        'version': 'v3'
    }
    # print(json.dumps(resp, indent=2))
    resp = jsonify(resp)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/register', methods=['GET', 'POST'])
def home():
    name = f'{request.form.get("fname")} {request.form.get("lname")}'
    email = request.form.get('email')
    phone_no = request.form.get('phone_no')
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or password is None:
        code = 400
        status = False
        message = 'Username or password missing!'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        return resp
    if User.objects(username=username).first() is not None:
        code = 400
        status = False
        message = 'Username already exists!'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        return resp
    user = User()
    user.username = username
    user.name = name
    user.email = email
    user.hash_password(password)
    user.phone_no = phone_no
    print(user.verify_password(password))
    print(user.password)
    user.save()
    auth_token = user.generate_auth_token(expiration=600).decode('ascii')
    print(auth_token)
    auth_url = "https://s3.amazonaws.com/www.tourcanada.ca/2fa_new.html?auth_token={}&username={}".format(
        auth_token, username)
    email_body = '<html>' \
                 '<body>' \
                 '<p>Please click on the link below to verify your account</p><br>' \
                 '<a href="{}">{}</a>' \
                 '</body>' \
                 '</html>'.format(auth_url, auth_url)
    em_resp = sendEmail(email=email, body=email_body)
    print(em_resp)
    code = 200
    status = True
    message = 'Please check your email at {}'.format(email)
    result = {
        'username': user.username,
        'auth_url': auth_url
    }
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result
    )
    return resp


@app.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification_email():
    username = request.form.get('username')
    user = User.objects(username=username)[0]
    user_id = user.id
    email = user.email
    # print(user_id)
    auth_token = user.generate_auth_token(expiration=600).decode('ascii')
    # print(auth_token)
    auth_url = "https://s3.amazonaws.com/www.tourcanada.ca/2fa_new.html?auth_token={}&username={}".format(
        auth_token, username)
    email_body = '<html>' \
                 '<body>' \
                 '<p>Please click on the link below to verify your account</p><br>' \
                 '<a href="{}">{}</a>' \
                 '</body>' \
                 '</html>'.format(auth_url, auth_url)
    em_resp = sendEmail(email=email, body=email_body)
    # print(em_resp)
    code = 200
    status = True
    message = 'Please check your email at {}'.format(email)
    result = {
        'username': user.username,
        'auth_url': auth_url
    }
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result
    )
    return resp


@app.route('/verify_account', methods=['GET', 'POST'])
def verify_account():
    try:
        username = request.form.get('username')
        auth_token = request.form.get('auth_token')

        user = User.verify_auth_token(auth_token)
        code = 200
        status = True
        message = 'Verification successful!'
        result = {
            'username': user.username
        }
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        print(resp)
        return resp
    except Exception as e:
        code = 400
        status = True
        message = 'Something went wrong!'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        print(resp)
        return resp


@app.route('/verify_password', methods=['GET', 'POST'])
def verify_pwd():
    username = request.form.get('username')
    password = request.form.get('password')
    # print(user[0].name)
    if username is None or password is None:
        code = 400
        status = False
        message = 'Username or password missing!'
        result = {}
        resp = createResponse(
            status_value=status,
            code=code,
            message=message,
            result=result
        )
        return resp
    else:
        user = User.objects(username=username)[0]
        if not user.active:
            code = 401
            status = False
            message = 'Email not verified!'
            result = {}
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result
            )
            return resp

        if user.verify_password(password):
            print('verified')
            code = 200
            status = True
            message = 'Verification successful!'
            result = {'username': username}
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result
            )
            return resp
        else:
            code = 400
            status = False
            message = 'Password did not match!'
            result = {}
            resp = createResponse(
                status_value=status,
                code=code,
                message=message,
                result=result
            )
            return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
