from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskblog.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=1,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField('Sign In')

    # custom validation : function name must be named as validate_'field name'
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('This username is exist.')

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This email is exist.')

class LoginForm(FlaskForm):
     email = StringField('Email',validators=[DataRequired(),Email()])
     password = PasswordField('Password',validators=[DataRequired()])
     remember = BooleanField('Remember Me')
     submit = SubmitField('Log In')
