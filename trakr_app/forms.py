from flask_wtf import FlaskForm
from sqlalchemy.sql import func
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from trakr_app import db
from trakr_app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(func.lower(User.username) == username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfileForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class ActionForm(FlaskForm):
    name = StringField('Action Name', validators=[DataRequired()])
    description = StringField('Action Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Add')

class DeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired()])
    location = SelectField('Device Location', validators=[DataRequired()])
    description = StringField('Device Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Add')

class EventForm(FlaskForm):
    device = SelectField('Device', validators=[DataRequired()])
    action = SelectField('Action', validators=[DataRequired()])
    event_dtm = DateTimeLocalField('Event Date and Time', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Add')