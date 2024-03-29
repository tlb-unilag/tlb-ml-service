import os
import requests
import json
import mailchimp_transactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

load_dotenv()


class EmailClient:
    def __init__(self, client_name=None):
        if client_name is None:
            client_name = os.getenv("EMAIL_CLIENT_NAME")
        if client_name == "zepto":
            self.api_key = os.getenv("Z_MAIL_KEY")
            self.send = zepto_send_mail
        else:
            self.api_key = os.getenv("M_MAIL_KEY")
            self.send = mail_chimp_send_email

    def send_mail(self, email, reset_token):
        return self.send(self.api_key, email, reset_token)


def mail_chimp_send_email(api_key, email, reset_token):
    """Send an email using the Mailchimp Transcational API.
    """
    message = {
        "from_email": "noreply@tlbproject.com.ng",
        "from_name": "Taro Leaf Blight Detection App",
        "subject": "Password reset token",
        "text": f"Your password reset token is: f{reset_token}. "
                f"Kindly use the token to reset your password in the App.",
        "to": [
            {
                "email": f"{email}",
                "type": "to"
            }
        ]
    }
    mailchimp = mailchimp_transactional.Client(api_key)
    try:
        response = mailchimp.messages.send({"message": message})
        if response[0]["status"] == "sent":
            return True
        return False
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return False


def zepto_send_mail(api_key, email, reset_token):
    url = "https://api.zeptomail.com/v1.1/email"

    message = f"<div> Your password reset token is: <b>{reset_token}</b> Kindly use " \
              f"the token to reset your password in the App.</div>"
    payload = {
        "from": {
            "address": "noreply@tlbproject.com.ng",
            "name": "Taro Leaf Blight Detection App"
        },
        "to": [
            {
                "email_address": {
                    "address": email,
                    "name": ""
                }
            }
        ],
        "subject": "Password reset token",
        "htmlbody": message
    }
    payload_json = json.dumps(payload)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': f"{api_key}",
    }
    try:
        response = requests.request("POST", url, data=payload_json, headers=headers)
        response = response.json()
        if response["message"] == "OK":
            return True
        return False
    except BaseException as e:
        response_helper(e)


def response_helper(e):
    if e == requests.exceptions.HTTPError:
        raise Exception("Http Error: %s" % e)
    if e == requests.exceptions.ConnectionError:
        raise Exception("Error Connecting: %s" % e)
    if e == requests.exceptions.Timeout:
        raise Exception("Timeout Error: %s" % e)
    if e == requests.exceptions.RequestException:
        raise Exception(e)
    else:
        raise Exception(e)
