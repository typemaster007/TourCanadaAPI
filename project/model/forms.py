__author__ = "Amogh Adithya"

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
import datetime
from project.model import dynamodb, scan_table
from wtforms import *
from wtforms.fields.html5 import EmailField, DateField
from flask import *
from werkzeug.datastructures import MultiDict


def luhn(ccn):  # Function that implements Luhn's Algorithm to validate card number
    c = [int(x) for x in ccn[::-2]]
    u2 = [(2 * int(y)) // 10 + (2 * int(y)) % 10 for y in ccn[-2::-2]]
    return sum(c + u2) % 10 == 0


class PaymentForm(FlaskForm):  # Payment Form Variables and Validations
    Cardname = StringField('Card Holder Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Cardnum = StringField('Card Number',
                          validators=[DataRequired(), Length(min=2, max=16)])

    expiry = DateField('Expiry Date',
                       validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Pay')

    cancel = SubmitField('Cancel')

    def validate_Cardnum(form, field):
        if (luhn(field.data) == False):
            raise ValidationError("Incorrect Credit Card Number, Please Re-Enter")

    def validate_expiry(form, field):
        date1 = datetime.datetime.strptime('2020-03-07', "%Y-%m-%d").date()
        if field.data < date1:
            raise ValidationError("Incorrect Date")
			

			

class RegistrationForm(Form):
    fname = StringField(label='First Name:',
                        validators=[validators.DataRequired(),
                                    validators.regexp('^[a-zA-Z]+$', message="Only characters allowed")])
    lname = StringField('Last Name:',
                        validators=[validators.DataRequired(),
                                    validators.regexp('^[a-zA-Z]+$', message="Only characters allowed")])
    username = StringField('Username:',
                           validators=[validators.DataRequired()])
    email = EmailField('Email:',
                        validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password:',
                             validators=[
                                 validators.DataRequired(),
                                 validators.Length(min=3, max=35),
                                 validators.EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm Password:',
                                    validators=[
                                        validators.DataRequired(), validators.Length(min=3, max=35)])
    submit = SubmitField('Register')

    def reset(self):
        blankData = MultiDict([('csrf', self.reset_csrf())])
        self.process(blankData)
