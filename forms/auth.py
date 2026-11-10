
from copy import copy

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    EmailField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
)


class BilingualForm(FlaskForm):
    translations = {}

    def __init__(self, *args, lang="en", **kwargs):
        if lang not in ("en", "fa"):
            raise ValueError("Unsupported language")

        super().__init__(*args, **kwargs)

        for field_name, languages in self.translations.items():
            field = getattr(self, field_name)
            translation = languages[lang]

            field.label.text = translation["label"]

            # Copy validators to avoid modifying shared objects.
            field.validators = [
                copy(validator)
                for validator in field.validators
            ]

            for validator, message in zip(
                field.validators,
                translation["messages"]
            ):
                validator.message = message


class LoginForm(BilingualForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )

    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")

    translations = {
        "username": {
            "en": {
                "label": "Username",
                "messages": [
                    "Username is required.",
                    "Username must be between 3 and 30 characters.",
                ],
            },
            "fa": {
                "label": "نام کاربری",
                "messages": [
                    "نام کاربری الزامی است.",
                    "نام کاربری باید بین ۳ تا ۳۰ کاراکتر باشد.",
                ],
            },
        },
        "password": {
            "en": {
                "label": "Password",
                "messages": ["Password is required."],
            },
            "fa": {
                "label": "رمز عبور",
                "messages": ["رمز عبور الزامی است."],
            },
        },
        "remember": {
            "en": {"label": "Remember me", "messages": []},
            "fa": {"label": "مرا به خاطر بسپار", "messages": []},
        },
        "submit": {
            "en": {"label": "Sign in", "messages": []},
            "fa": {"label": "ورود", "messages": []},
        },
    }


class RegisterForm(BilingualForm):
    name = StringField(
        "Full name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
        ],
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password"),
        ],
    )

    submit = SubmitField("Create account")

    translations = {
        "name": {
            "en": {
                "label": "Full name",
                "messages": [
                    "Full name is required.",
                    "Full name must be between 2 and 100 characters.",
                ],
            },
            "fa": {
                "label": "نام و نام خانوادگی",
                "messages": [
                    "وارد کردن نام الزامی است.",
                    "نام باید بین ۲ تا ۱۰۰ کاراکتر باشد.",
                ],
            },
        },
        "username": {
            "en": {
                "label": "Username",
                "messages": [
                    "Username is required.",
                    "Username must be between 3 and 30 characters.",
                ],
            },
            "fa": {
                "label": "نام کاربری",
                "messages": [
                    "نام کاربری الزامی است.",
                    "نام کاربری باید بین ۳ تا ۳۰ کاراکتر باشد.",
                ],
            },
        },
        "email": {
            "en": {
                "label": "Email address",
                "messages": [
                    "Email is required.",
                    "Please enter a valid email address.",
                ],
            },
            "fa": {
                "label": "آدرس ایمیل",
                "messages": [
                    "آدرس ایمیل الزامی است.",
                    "آدرس ایمیل معتبر نیست.",
                ],
            },
        },
        "password": {
            "en": {
                "label": "Password",
                "messages": [
                    "Password is required.",
                    "Password must be at least 8 characters.",
                ],
            },
            "fa": {
                "label": "رمز عبور",
                "messages": [
                    "رمز عبور الزامی است.",
                    "رمز عبور باید حداقل ۸ کاراکتر باشد.",
                ],
            },
        },
        "confirm_password": {
            "en": {
                "label": "Confirm password",
                "messages": [
                    "Please confirm your password.",
                    "Passwords do not match.",
                ],
            },
            "fa": {
                "label": "تکرار رمز عبور",
                "messages": [
                    "تکرار رمز عبور الزامی است.",
                    "رمزهای عبور مطابقت ندارند.",
                ],
            },
        },
        "submit": {
            "en": {"label": "Create account", "messages": []},
            "fa": {"label": "ایجاد حساب", "messages": []},
        },
    }
