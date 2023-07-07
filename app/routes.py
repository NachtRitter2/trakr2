from flask import render_template
from datetime import datetime, timedelta
from app import app

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

    posts = [
            {
                'author': {'username':'Birdie'},
                'body': 'Beautiful day in the sunshine!'
            },
            {
                'author': {'username':'Giovanna'},
                'body': 'This mouse toy is sooo cooool!'
            }
        ]

    return render_template('index.html', title='CatHome', user=user, measures=measures)
