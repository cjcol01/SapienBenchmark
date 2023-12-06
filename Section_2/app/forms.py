from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from .models import User

# Registration form
class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
        render_kw={"placeholder": "Email"},
    )
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_name = User.query.filter_by(username=username.data).first()
        if existing_user_name:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


# Login form
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(min=4, max=50)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")
