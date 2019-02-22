from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.auth.models import User
from app import bcrypt
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=2, max=20, message="Must be more than 2 and less than 20 characters")]) # () because class needs to activate
    email = StringField("Email", validators=[
        DataRequired(),
        Email(),
        Length(min=2, max=30, message="Must be more than 2 and less than 30 characters")])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo('password')]) # Name of the variable, not passing the whole object there
    submit = SubmitField("Register")

# validate_username is reserverd for autovalidator, for field username
# Name of parameter can be any but it encodes the field anyway
    def validate_username(self, username): # here, username is a form field object
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"User '{username.data}' already exists")
        return

    def validate_email(self, email):
        lookup_email = User.query.filter_by(email=email.data).first()
        if lookup_email:
            raise ValidationError(f"Email '{email.data}' is already registered")
        return


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Always Remember Me")
    submit = SubmitField("Log in")

    def validate_email(self, email):
        lookup_email = User.query.filter_by(email=email.data).first()
        if not lookup_email:
            raise ValidationError(f"Email '{email.data}' is not registered")
        return

    def validate_password(self, password):
        lookup_by_email = User.query.filter_by(email=self.email.data).first()
        print(bcrypt.check_password_hash(lookup_by_email.password, password.data))
        if lookup_by_email and not bcrypt.check_password_hash(lookup_by_email.password, password.data):
            raise ValidationError("Password is not correct!")
        return

class UpdateAccount(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=2, max=20, message="Must be more than 2 and less than 20 characters")])
    email = StringField("Email", validators=[
        DataRequired(),
        Email(),
        Length(min=2, max=30, message="Must be more than 2 and less than 30 characters")])
    avatar = FileField("Upload your avatar", validators=[FileAllowed(['jpg','png','jpeg', 'gif'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data!=current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f"Username '{username.data}' is already occupied")

    def validate_email(self, email):
        if email.data!=current_user.email:
            lookup_email = User.query.filter_by(email=email.data).first()
            if lookup_email:
                raise ValidationError(f"Email address '{email.data}' is registered for another account")
