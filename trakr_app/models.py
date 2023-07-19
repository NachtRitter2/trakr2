from hashlib import md5
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from trakr_app import db, login
from flask_login import UserMixin


class User(UserMixin,db.Model):
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.relationship('Location', backref='editor', lazy='dynamic')
    sensor = db.relationship('Sensor', backref='editor', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return (self.username)
    
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(
                digest, size)
    
    
class Location(db.Model):
    name = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    description = db.Column(db.String(140))
    is_obsolete = db.Column(db.Boolean, default=False)
    updated_dtm = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(64), db.ForeignKey('user.username'))
    sensor = db.relationship('Sensor', backref='place', lazy='dynamic')
    reading = db.relationship('Reading', backref='place', lazy='dynamic')

    def __repr__(self):
        return '<Location {}>'.format(self.name)
    
class Sensor(db.Model):
    serial_nr = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    lower_limit = db.Column(db.Integer)
    upper_limit = db.Column(db.Integer)
    location = db.Column(db.String(64), db.ForeignKey('location.name'))
    updated_dtm = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(64), db.ForeignKey('user.username'))
    reading = db.relationship('Reading', backref='sensor', lazy='dynamic')

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)
    
class Reading(db.Model):
    location = db.Column(db.String(64), db.ForeignKey('location.name'))
    serial_nr = db.Column(db.Integer, db.ForeignKey('sensor.serial_nr'), primary_key=True)
    reading_dtm = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    value = db.Column(db.Float)

    def __repr__(self):
        return '<Reading {}: {} at {}>'.format(self.serial_nr, self.reading_dtm, self.value)

@login.user_loader
def load_user(username):
    return User.query.get(username)
