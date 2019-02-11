from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, jsonify, abort, flash
from config import Config
from flask_login import login_required, login_user, logout_user, current_user
from model.user import User
from passlib.hash import pbkdf2_sha256
from model.forms.signup import SignupForm

routes = Blueprint('routes', __name__)


@routes.route('/<path:path>')
def static_files(path):
    return send_from_directory(Config.STATIC_DIR, path)


@routes.route('/app')
@login_required
def app():
    return render_template('app/index.html')


@routes.route('/')
def index():
    return render_template('templates/index.html')


@routes.route('/accounts/login', methods=['POST'])
def auth_login():
    username_email = request.form.get('username-or-email')
    password = request.form.get('password')
    user = User.get_user(username_email)
    if user:
        if pbkdf2_sha256.verify(password, user.password_hash):
            login_user(user)
            return redirect(url_for('routes.app'))

    flash('Incorrect username or password.', 'alert alert-danger alert-dismissible fade show')
    return redirect(url_for('routes.app'))


@routes.route('/accounts/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.app'))
    next = request.args.get('next')
    return render_template('templates/login.html', next=next)


@routes.route('/accounts/logout', methods=['GET'])
@login_required
def logout():
    flash('You have logged out.', 'alert alert-success alert-dismissible fade show')
    logout_user()
    return redirect(url_for('routes.app'))


@routes.route('/accounts/signup', methods=['POST'])
def signup_process():
    form = SignupForm()
    if not form.validate():
        return render_template('templates/signup.html', form=form)
    password_hash = pbkdf2_sha256.hash(form.password.data)
    user = User.create_user(form.username.data, form.email.data, password_hash)
    flash('You have registered an account successfully.', 'alert alert-success alert-dismissible fade show')
    return redirect(url_for('routes.login'))
    # TODO: haveibeenpwned API to check for weak passwords and suggest to the user to use a different password
    # - https://haveibeenpwned.com/API/v2


@routes.route('/accounts/signup', methods=['GET'])
def signup():
    form = SignupForm()
    return render_template('templates/signup.html', form=form)


@routes.route('/about')
def about():
    # TODO: Create a template for this
    return 'about page'


@routes.route('/accounts')
# @login_required # TODO re-enable this again
def accounts():
    # TODO: Create a template to render this with flash messages
    # TODO: make this accessible only to admins in the database
    if current_user.is_authenticated and current_user.id == 'bob@example.com' or True:
        users = User.get_users()
        users_list = []
        for user in users:
            users_list.append({'username': user['username'], 'email': user['email']})
        return jsonify(users_list)
    else:
        abort(403)


@routes.route('/policies/tos')
def tos():
    return 'Terms of service ...'


@routes.route('/delete')
def delete():
    # TODO: Remove this
    instances = Config.mongo_client.users.instances
    instances.remove({})
    return 'Deleted all users'