# Twilio Account Security Demo Site - 2FA and Phone Verification in Python

A Python/Flask implementation demonstrating Twilio's Account Security APIs:

* [Lookup](https://www.twilio.com/docs/lookup/api) (phone number information)
* [Verify](https://www.twilio.com/docs/verify/api) (phone verification)
* [Authy](https://www.twilio.com/docs/authy/api) (two factor authentication)

## Setup

### Pre-Reqs

Follow our instructions for [how to set up your Python and Flask development environment](https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment). 

**This project uses Python3.**

### Installation

Quick copy for unix:
```
git clone https://github.com/robinske/account-security-python-demo
cd account-security-python-demo
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp demo.env.example demo.env
cp db.json.example db.json
export FLASK_ENV=development
flask run
```

#### Step by step installation:

Clone this repo
```
git clone https://github.com/robinske/account-security-python-demo
```

If you're not familiar with Python virtual environments, [follow our tutorial for setting up your local Python environment](https://www.twilio.com/docs/usage/quickstart/devenvironment-python#installing-flask-and-twilio-python). Navigate into the project folder and create your virtual environment.

```
cd account-security-python-demo

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
```

Copy `demo.env.example` to `demo.env`. This is where we'll store sensitive data in [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
```
cp demo.env.example demo.env
cp db.json.example db.json
```

Open the demo.env file and fill in your credentials. You can find these in the [Twilio Console](https://www.twilio.com/console). Create an Authy Application (`AUTHY_API_KEY`) in the [Authy Console](https://www.twilio.com/console/authy/applications).

### Run the application
```
export FLASK_ENV=development
flask run
```

Or on Windows cmd:
```
set FLASK_ENV=development
flask run
```
Navigate to http://localhost:5000. If your credentials are set up correctly you'll soon get a message that the app is up!

### License
MIT
