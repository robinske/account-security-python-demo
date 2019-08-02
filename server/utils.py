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
    client = Client(app.config['TWILIO_ACCT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    SERVICE = app.config['VERIFY_SERVICE_SID']
    
    verification = client.verify \
        .services(SERVICE) \
        .verifications \
        .create(to=phone_number, channel=channel, locale=locale)
    
    print("Verification sent to {} with SID: '{}'".format(phone_number, verification.sid))
    return verification.sid


def check_verification(phone_number, token):
    client = Client(app.config['TWILIO_ACCT_SID'], app.config['TWILIO_AUTH_TOKEN'])
    SERVICE = app.config['VERIFY_SERVICE_SID']
    verification_check = client.verify \
        .services(SERVICE) \
        .verification_checks \
        .create(to=phone_number, code=token)
    
    return verification_check.status


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
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])
    
    user = authy_api.users.create(email, phone_number, country_code)
    if user.ok():
        _save_user(email, country_code, phone_number, user.id)
        return user.id
    else:
        flash("Error registering user with Authy: '{}'".format(user.errors()))
    
    
def send_sms_token(authy_id, locale):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    sms = authy_api.users.request_sms(authy_id, {'force': True, 'locale': locale})

    return sms.ok()


def send_voice_token(authy_id, locale):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    call = authy_api.users.request_call(authy_id, {'force': True, 'locale': locale})

    return call.ok()


def verify_authy_token(authy_id, token):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    try:
        verification = authy_api.tokens.verify(authy_id, token)
    except Exception as e:
        flash("Error validating token: {}".format(e))
        return False

    return verification.ok()


def send_push_auth(authy_id):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    details = {}
    details['Account Number'] = '123456'

    hidden_details = {}
    hidden_details['ip_address'] = '100.12.345.67'

    message = "Push authorization request from Authy Demo App."
    seconds_to_expire = 120

    response = authy_api.one_touch.send_request(
        authy_id,
        message,
        seconds_to_expire=seconds_to_expire,
        details=details,
        hidden_details=hidden_details)
    
    if response.ok():
        return (response.get_uuid(), None)
    else:
        return (None, resp.errors()['message'])


def check_push_status(uuid):
    authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

    resp = authy_api.one_touch.get_approval_status(uuid)
    if resp.ok():
        return resp.content['approval_request']['status']
    else:
        return "pending"

