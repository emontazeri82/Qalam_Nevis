from flask_wtf import FlaskForm
from wtforms import (
      StringField, PasswordField, 
      BooleanField, SubmitField,
      EmailField, 
)
from wtforms.validators import (
  DataRequired, Optional,
  Length,
  Email,
  EqualTo,
)
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = EmailField("Email", validators=[Optional(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")