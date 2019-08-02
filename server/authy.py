from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from functools import wraps
from flask import current_app as app
from . import utils
from server.forms import RegisterForm, ChallengeForm, LoginForm, LocaleForm


bp = Blueprint('authy', __name__, url_prefix='/authy')


@bp.before_app_request
def load_logged_in_user():
    g.authy_id = session.get('authy_id')
    g.email = session.get('email')
    g.twofa = session.get('twofa')


def login_required(view):
    """
    View decorator that redirects anonymous users to the login page.
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.email is None:
            return redirect(url_for('authy.login'))
        return view(**kwargs)
    return wrapped_view


def twofa_required(view):
    """
    View decorator that redirects unverified users back to the 2FA page.
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if not g.twofa:
            flash("Complete 2FA in order to view protected content.")
            return redirect(url_for('authy.twofa'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        country_code = form.country_code.data
        phone_number = form.phone_number.data

        authy_id = utils.register_authy_user(email, country_code, phone_number)
        session['authy_id'] = authy_id
        session['email'] = email
        return redirect(url_for('authy.twofa'))

    return render_template('register.html', form=form, g=g)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('email') is not None:
        return redirect(url_for('authy.twofa'))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        
        authy_id = utils.get_authy_id(email)
        if authy_id is not None:
            session['authy_id'] = authy_id
            session['email'] = email
            return redirect(url_for('authy.twofa'))
        else:
            flash("Please register")
            return redirect(url_for("authy.register"))

    return render_template('login.html', form=form)


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route('/2fa', methods=('GET', 'POST'))
@login_required
def twofa():
    challenge_form = ChallengeForm(request.form)
    locale_form = LocaleForm(request.form)
    session['twofa'] = False

    if challenge_form.validate_on_submit():
        token = challenge_form.token.data
        authy_id = session['authy_id']

        valid = utils.verify_authy_token(authy_id, token)
        if valid:
            session['twofa'] = True
            return redirect(url_for("authy.protected"))
        else:
            flash("Incorrect token. Please try again.")
    
    return render_template('2fa.html', form=challenge_form, locale_form=locale_form)


@bp.route('/sms', methods=['POST'])
def send_sms():
    authy_id = session['authy_id']
    locale = request.form.get('locale', 'en')

    success = utils.send_sms_token(authy_id, locale)
    return jsonify({"success": success})


@bp.route('/voice', methods=['POST'])
def send_voice_call():
    authy_id = session['authy_id']
    locale = request.form.get('locale', 'en')

    success = utils.send_voice_token(authy_id, locale)
    return jsonify({"success": success})


@bp.route('/push', methods=['POST'])
def send_push():
    authy_id = session['authy_id']
    (uuid, errors) = utils.send_push_auth(authy_id)
    if uuid:
        return jsonify({
            "success": True,
            "uuid": uuid
        })
    else:
        flash("Error sending authorization. {}".format(errors))
        return jsonify({"success": False})


@bp.route('/push/status', methods=['GET', 'POST'])
def push_status():
    uuid = request.args.get('uuid')
    status = utils.check_push_status(uuid)
    if status is 'approved':
        session['twofa'] = True
    return jsonify({"status": status})


@bp.route('/protected', methods=['GET'])
@login_required
@twofa_required
def protected():
    message = "Congratulations! You have successfully implemented Authy and are now viewing protected content"
    return render_template("protected.html", message=message)