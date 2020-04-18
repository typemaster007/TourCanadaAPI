__author__ = "Daksh Patel"
import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Tour Canada <ticket-confirmation@tourcanada.awsapps.com>"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = "dbp2298@gmail.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = "Ticket Confirmation to {}".format('LOCATION')

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Hello {},\n"
             "Your ticket (TICKET ID = {}) to {} is confirmed.".format('NAME', 'TICKET_ID', 'LOCATION'))

# The HTML body of the email.
BODY_HTML = """<html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</head>
<body>
  <h5>Hello {}</h5>
  <p>Your ticket (Ticket id: {}) to {} is confirmed. Have a happy and safe journey</p>

  <small>Thank you for using Tour Canada!</small>
</body>
</html>""".format('NAME', 'TICKET_ID', 'LOCATION')

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
ACCESS_KEY="AKIAI4QN3WUXE4R3ID5Q"
SECRET_KEY="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"
client = boto3.client('ses',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      region_name=AWS_REGION)
# response = client.verify_email_identity(
#   EmailAddress = 'dbp2298@gmail.com'
# )

# print(response)
# Try to send the email.
try:
    # Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])