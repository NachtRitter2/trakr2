from flask import render_template, flash, redirect, url_for
from datetime import datetime, timedelta
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data.lower(), form.remember_me.data
        ))
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)
