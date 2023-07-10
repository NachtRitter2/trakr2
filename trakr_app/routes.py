from flask import render_template, flash, redirect, url_for, request
from datetime import datetime, timedelta
from trakr_app import app
from trakr_app.forms import LoginForm

@app.before_request
def before():
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


@app.route('/')
@app.route('/index')
def index():
    app.logger.debug('Entered index code section')

    user = {'username':'Dasher'}

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

    return render_template('index.html', title='CatHome', user=user, measures=measures)

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug('Entered login code section')
    
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data.lower(), form.remember_me.data
        ))
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)
