from wsgi import app
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import os
from werkzeug.utils import secure_filename
from app.models import db, User
from app.forms import RegistrationForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm, UploadFileForm
from app.email import send_password_reset_email


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = []
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
    return render_template('index.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Form was submitted and data looks good. Create new user.
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('forms/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('forms/reset_password.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('buffer', type='password_reset'))
    return render_template('forms/reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/buffer/<type>')
def buffer(type):
    redirect_url = url_for('index')
    if type in ['album_post', 'changes_successful', 'add_content_successful']:
        redirect_url = url_for('admin')
    elif type in ['contact_successful', 'contact_request', 'password_reset']:
        redirect_url = url_for('index')
    return render_template('buffer.html', type=type, redirect_url=redirect_url)


@login_required
@app.route('/test_form', methods=['GET','POST'])
def test_form():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UploadFileForm()
    if form.validate_on_submit():
        print('made it here')

        # file upload logic
        f = form.file.data
        if f.mimetype not in app.config['ACCEPTABLE_FILE_TYPES']:
            return redirect(url_for('index'))

        filename = secure_filename(form.file.data.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

        # if resource is tied to a database record, the logic would go here.

        # new_record = DataModel(<params>)
        # db.session.add(new_record)
        # db.session.commit()

        return redirect(url_for('index'))
    return render_template('forms/upload_file.html', form=form)


@app.route('/api_example')
def api_example():
    data = request.args.get('id')
    if data is None:
        return jsonify({'message': 'No id was passed. Try /api_example?id=<your favorite number>'})
    else:
        return jsonify({'message': 'The id {} was passed to the API.'.format(data)})

@app.route('/api_example2')
def api_example2():
    return jsonify({'Message': 'This data was fetched with an ajax call after the page loaded.'})

@login_required
@app.route('/admin')
def admin():
    if not (current_user.is_authenticated and User.query.filter_by(id=current_user.id).first().admin):
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin.html', users=users)
