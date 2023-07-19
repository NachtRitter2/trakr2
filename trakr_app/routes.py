from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql import func
from werkzeug.urls import url_parse
from datetime import datetime, timedelta
from trakr_app import app, db
from trakr_app.forms import LoginForm, RegistrationForm, EditProfileForm
from trakr_app.models import User, Location, Sensor

@app.before_request
def before_request():
    # For debugging purposes, read out the url and the attributes
    url = 'full url: ' + request.url
    app.logger.debug(url)

    root_url = 'root url: ' + request.url_root
    app.logger.debug(root_url)

    path = 'path: ' + request.path
    app.logger.debug(path)

    # Get the env variable if it exists
    if "REQUEST_URI" in request.environ.keys():
        path = 'env uri: ' + request.environ["REQUEST_URI"]
        app.logger.debug(path)
    
    values = 'values: '
    if len(request.values) == 0:
        values += '(None)'
    for key in request.values:
        values += key + ': ' + request.values[key] + ', '
    app.logger.debug(values)

    # Capture user's visit time
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    app.logger.debug('Entered index code section')

    measures = [
        {
            'location': 'Bedroom1',
            'article': 'RoomSensor',
            'type': 'TemperatureC',
            'value': '32',
            'datetime': (datetime.now()-timedelta(minutes = 5)).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'location': 'LivingRoom',
            'article': 'RoomSensor',
            'type': 'TemperatureC',
            'value': '37',
            'datetime': (datetime.now()-timedelta(minutes = 10)).strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    return render_template('index.html', title='Cats Dev Home', measures=measures)

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug('Entered login code section')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == form.username.data.lower()).first()
        app.logger.info(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.get_or_404(username)
    locations = Location.query.all()
    sensors = Sensor.query.all()
    return render_template('user.html', user=user, locations=locations, sensors=sensors)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)