import boto3
import requests
from datetime import datetime
import os

# Create a new SES resource and specify a region
ses = boto3.client(
    'ses',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key'),
    region_name=os.getenv('region_name')
)
# Define the sender and recipient
SENDER = "Raspberry PI Health Check <sender@gmail.com>"
RECIPIENTS = ["receiver1@gmail.com", "receiver2@gmail.com"]

# Specify a configuration set if you have one
CONFIGURATION_SET = "ConfigSet"

# The subject line for the email
SUBJECT = "Server Down"

# The email body for recipients with non-HTML email clients
BODY_TEXT = "This email was sent with Amazon SES using the AWS SDK for Python (Boto3)."

# The HTML body of the email
BODY_HTML = """<html>
<head></head>
<body>
  <h1>API Server is Down</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://boto3.amazonaws.com/v1/documentation/api/latest/index.html'>AWS SDK for Python (Boto3)</a>.
  </p>
</body>
</html>
"""

# The character encoding for the email
CHARSET = "UTF-8"


# Try to send the email
def send_email(api):
    try:
        # Provide the contents of the email
        response = ses.send_email(
            Destination={
                'ToAddresses': RECIPIENTS
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
                    'Data': SUBJECT + " for " + api[1] + "!!! " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            },
            Source=SENDER
        )
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent for " + api[1] + "! Message ID:"),
        print(response['MessageId'])


api_urls = [
    ["api_url_1", "Service1"],
    ["api_url_2", "Service2"]
]


def check_api_status():
    for url in api_urls:
        try:
            response = requests.get(url[0])
            if response.status_code == 200:
                print("SUCCESS", url[1])
            else:
                send_email(url)
        except requests.exceptions.RequestException as e:
            send_email(url)


check_api_status()
