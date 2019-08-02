from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask import current_app as app
from server.forms import LookupForm, StartVerifyForm, VerifyForm
from . import utils
from twilio.rest import Client


bp = Blueprint('verification', __name__, url_prefix='/verification')


@bp.route('/', methods=('GET', 'POST'))
def verify():
    lookup_form = LookupForm(request.form)
    verify_form = StartVerifyForm(request.form)

    lookup_data=None

    if lookup_form.validate_on_submit():
        country_code = lookup_form.country_code.data
        phone_number = lookup_form.phone_number.data
        full_phone = "+{}{}".format(country_code, phone_number)
        lookup_data = utils.lookup(phone_number=full_phone)

    return render_template('verification.html', lookup_form=lookup_form, verify_form=verify_form, lookup_data=lookup_data)


@bp.route('/start', methods=('GET', 'POST'))
def start_verification():
    form = StartVerifyForm(request.form)

    if form.validate_on_submit():
        country_code = form.country_code.data
        phone_number = form.phone_number.data
        full_phone = "+{}{}".format(country_code, phone_number)
        channel = form.channel.data
        locale = form.locale.data

        utils.start_verification(phone_number=full_phone, channel=channel, locale=locale)

        # save to session for checking token later
        session['phone_number'] = full_phone

        return redirect(url_for('verification.check'))

    return redirect('/')


@bp.route('/check', methods=('GET', 'POST'))
def check():
    form = VerifyForm(request.form)

    if form.validate_on_submit():
        phone_number = session['phone_number']
        token = form.token.data
        verification_status = utils.check_verification(phone_number, token)

        if verification_status == "approved":
            return redirect(url_for("verification.protected"))
        else:
            flash("Incorrect token. Please try again.")

    return render_template('verification_check.html', form=form)


@bp.route('/protected', methods=['GET'])
def protected():
    message = "Congratulations! You have successfully verified your phone number."
    return render_template("protected.html", message=message)

