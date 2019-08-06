import json

from flask import flash
from flask import current_app as app

from twilio.rest import Client
from authy.api import AuthyApiClient


def lookup(phone_number):
    client = Client(app.config['TWILIO_ACCT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    resp = client.lookups.phone_numbers(phone_number).fetch(type=['carrier'])
    
    return resp.carrier


def start_verification(phone_number, channel, locale):
    """
    Send a phone verification to the provided number.
    Return the verification SID
    """
    client = Client(app.config['TWILIO_ACCT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    SERVICE = app.config['VERIFY_SERVICE_SID']

    # TODO SEND VERIFICATION
    # https://www.twilio.com/docs/verify/api/verification
    
    return "TODO - verification SID"


def check_verification(phone_number, token):
    """
    CHECK a phone verification with the provided token.
    Return the verification status
    """
    client = Client(app.config['TWILIO_ACCT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    SERVICE = app.config['VERIFY_SERVICE_SID']
    
    # TODO CHECK VERIFICATION
    # https://www.twilio.com/docs/verify/api/verification-check

    return "TODO - verification status"


def _save_user(email, country_code, phone_number, authy_id):
    user_details = {
        "cc": country_code,
        "pn": phone_number,
        "password": "pass",
        "authy_id": authy_id
    }

    users = None
    with open('db.json', 'r') as jf:
        users = json.load(jf).get("users")
        users[email] = user_details
    
    with open('db.json', 'w') as db:
        db.write(json.dumps({"users": users}))


def get_authy_id(email):
    try:
        with open('db.json', 'r') as jf:
            users = json.load(jf).get("users")
            return users[email]['authy_id']
    except:
        return None


def register_authy_user(email, country_code, phone_number):
    """
    Register the user with Authy.
    Returns the Authy ID.
    """
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])
    
    # TODO - register Authy user
    # https://github.com/twilio/authy-python#users
    # API reference: https://www.twilio.com/docs/authy/api/users#enabling-new-user
    
    return "TODO - authy ID"
    
    
def send_sms_token(authy_id, locale):
    """
    Send an SMS token
    Returns a tuple of (success: Boolean, message: String) 
    """
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    # TODO - send SMS
    # https://github.com/twilio/authy-python#sending-sms-2fa-tokens
    # API reference: https://www.twilio.com/docs/authy/api/one-time-passwords#request-a-one-time-password

    return (False, "TODO - implement this")


def send_voice_token(authy_id, locale):
    """
    Send an Voice token
    Returns a tuple of (success: Boolean, message: String) 
    """
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    # TODO - send Voice call
    # https://github.com/twilio/authy-python#sending-call-2fa-tokens
    # API reference: https://www.twilio.com/docs/authy/api/one-time-passwords#request-a-one-time-password
    
    return (False, "TODO - implement this")


def verify_authy_token(authy_id, token):
    """
    Check the token
    Returns success boolean
    """
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    # TODO - check token
    # https://github.com/twilio/authy-python#verifying-tokens
    # API reference: https://www.twilio.com/docs/authy/api/one-time-passwords#verify-a-one-time-password

    return False # TODO


def send_push_auth(authy_id):
    """
    Starts a push authentication
    Returns a tuple of (push_uuid: String, errors: String) 
    """
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    # TODO start push auth
    # https://github.com/twilio/authy-python#send-approval-request
    # API reference: https://www.twilio.com/docs/authy/api/push-authentications#create-an-approval-request

    return (None, "TODO - implement this")


def check_push_status(uuid):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    resp = authy_api.one_touch.get_approval_status(uuid)
    if resp.ok():
        return resp.content['approval_request']['status']
    else:
        return "pending"

