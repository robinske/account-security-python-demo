from flask_wtf import FlaskForm
from wtforms import (
    IntegerField, 
    PasswordField, 
    SelectField, 
    StringField, 
    validators
)


class LookupForm(FlaskForm):
    """Form used to lookup a phone number"""
    country_code = StringField(
        'Country Code', 
        validators=[validators.InputRequired()])
    phone_number = StringField(
        'Phone #', 
        validators=[validators.InputRequired()])


class StartVerifyForm(FlaskForm):
    """Form used for registering new users"""
    country_code = StringField(
        'Country Code', 
        validators=[validators.InputRequired()])
    phone_number = StringField(
        'Phone', 
        validators=[validators.InputRequired()])
    channel = SelectField(
        'Channel',
        choices=[('sms', 'SMS'),('call', 'Call')],
        default='sms')
    locale = SelectField(
        'Language',
        choices=[
            ('af', 'Afrikaans'),
            ('ar', 'Arabic'),
            ('ca', 'Catalan'),
            ('zh', 'Chinese'),
            ('zh-CN', 'Chinese (Mandarin)'),
            ('zh-HK', 'Chinese (Cantonese)'),
            ('hr', 'Croatian'),
            ('cs', 'Czech'),
            ('da', 'Danish'),
            ('nl', 'Dutch'),
            ('en', 'English'),
            ('fi', 'Finnish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('el', 'Greek'),
            ('he', 'Hebrew'),
            ('hi', 'Hindi'),
            ('hu', 'Hungarian'),
            ('id', 'Indonesian'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('ms', 'Malay'),
            ('nb', 'Norwegian'),
            ('pl', 'Polish'),
            ('pt-BR', 'Portuguese - Brazil'),
            ('pt', 'Portuguese'),
            ('ro', 'Romanian'),
            ('ru', 'Russian'),
            ('es', 'Spanish'),
            ('sv', 'Swedish'),
            ('tl', 'Tagalog')
        ],
        default='en'
    )


class LocaleForm(FlaskForm):
    locale = SelectField(
        'Language',
        choices=[
            ('af', 'Afrikaans'),
            ('ar', 'Arabic'),
            ('ca', 'Catalan'),
            ('zh', 'Chinese'),
            ('zh-CN', 'Chinese (Mandarin)'),
            ('zh-HK', 'Chinese (Cantonese)'),
            ('hr', 'Croatian'),
            ('cs', 'Czech'),
            ('da', 'Danish'),
            ('nl', 'Dutch'),
            ('en', 'English'),
            ('fi', 'Finnish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('el', 'Greek'),
            ('he', 'Hebrew'),
            ('hi', 'Hindi'),
            ('hu', 'Hungarian'),
            ('id', 'Indonesian'),
            ('it', 'Italian'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('ms', 'Malay'),
            ('nb', 'Norwegian'),
            ('pl', 'Polish'),
            ('pt-BR', 'Portuguese - Brazil'),
            ('pt', 'Portuguese'),
            ('ro', 'Romanian'),
            ('ru', 'Russian'),
            ('es', 'Spanish'),
            ('sv', 'Swedish'),
            ('tl', 'Tagalog')
        ],
        default='en'
    )


class VerifyForm(FlaskForm):
    """Form used to verify SMS tokens"""
    token = StringField(
        'Verification token',
        validators=[
            validators.InputRequired(),
            validators.Length(min=4, max=10)
        ]
    )


class RegisterForm(FlaskForm):
    """Form used for registering new users"""
    email = StringField(
        'Email', 
        validators=[validators.InputRequired(), 
                    validators.Email()])
    ## DANGER THIS IS A DEMO AND THIS IS NOT REAL PASSWORD STORAGE
    password = PasswordField(
        'Password', 
        validators=[validators.InputRequired()])
    country_code = StringField(
        'Country Code', 
        validators=[validators.InputRequired()])
    phone_number = StringField(
        'Phone', 
        validators=[validators.InputRequired()])


class LoginForm(FlaskForm):
    """Form used for registering new users"""
    email = StringField(
        'Email', 
        validators=[validators.InputRequired(), 
                    validators.Email()])
    ## DANGER THIS IS A DEMO AND THIS IS NOT REAL PASSWORD STORAGE
    password = PasswordField(
        'Password', 
        validators=[validators.InputRequired()])


class ChallengeForm(FlaskForm):
    """Form used to verify Authy codes"""
    token = StringField(
        'Verification token',
        validators=[
            validators.InputRequired(),
            validators.Length(min=4, max=10)
        ]
    )
