
from datetime import datetime, timezone

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from forms.auth import LoginForm, RegisterForm
from models import Role, User, UserRole
from models.extensions import db


auth_bp = Blueprint("auth", __name__)


def valid_language(lang: str) -> None:
    if lang not in ("en", "fa"):
        abort(404)


@auth_bp.route("/<lang>/login", methods=["GET", "POST"])
def login(lang: str) -> ResponseReturnValue:
    valid_language(lang)

    form = LoginForm(lang=lang)
    form.auth_errors = []

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        stmt = select(User).where(
            func.lower(User.username) == username.lower()
        )
        user = db.session.scalar(stmt)

        password_valid = (
            user is not None
            and check_password_hash(
                user.password_hash,
                password,
            )
        )

        if password_valid and user.is_active:
            role_codes = {
                user_role.role.code
                for user_role in user.user_roles
            }

            if "admin" in role_codes or "editor" in role_codes:
                destination = "admin_dashboard"

            elif "writer" in role_codes:
                destination = "writer_dashboard"

            else:
                destination = None
                form.auth_errors.append(
                    "حساب شما مجوز دسترسی ندارد."
                    if lang == "fa"
                    else "Your account does not have an assigned access role."
                )

            if destination is not None:
                logged_in = login_user(
                    user,
                    remember=bool(form.remember.data),
                )

                if logged_in:
                    user.last_login_at = datetime.now(timezone.utc)

                    try:
                        db.session.commit()
                    except Exception:
                        db.session.rollback()
                        current_app.logger.exception(
                            "Failed to update last login time"
                        )

                    return redirect(
                        url_for(destination, lang=lang)
                    )

                form.auth_errors.append(
                    "ورود به حساب امکان‌پذیر نیست."
                    if lang == "fa"
                    else "Unable to sign in."
                )

        else:
            form.auth_errors.append(
                "نام کاربری یا رمز عبور اشتباه است."
                if lang == "fa"
                else "Invalid username or password."
            )

    return render_template(
        "auth/login.html",
        lang=lang,
        form=form,
    )


@auth_bp.route("/<lang>/register", methods=["GET", "POST"])
def register(lang: str) -> ResponseReturnValue:
    valid_language(lang)

    form = RegisterForm(lang=lang)
    form.auth_errors = []

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        display_name = form.name.data.strip()

        username_stmt = select(User).where(
            func.lower(User.username) == username.lower()
        )

        existing_user = db.session.scalar(username_stmt)

        if existing_user is not None:
            form.username.errors.append(
                "این نام کاربری قبلاً ثبت شده است."
                if lang == "fa"
                else "This username is already taken."
            )

        email_stmt = select(User).where(
            func.lower(User.email) == email.lower()
        )

        existing_email = db.session.scalar(email_stmt)

        if existing_email is not None:
            form.email.errors.append(
                "این ایمیل قبلاً ثبت شده است."
                if lang == "fa"
                else "This email is already taken."
            )

        if not form.username.errors and not form.email.errors:
            writer_stmt = select(Role).where(
                Role.code == "writer"
            )

            writer_role = db.session.scalar(writer_stmt)

            if writer_role is None:
                current_app.logger.error(
                    "Writer role missing from database"
                )

                form.auth_errors.append(
                    "ثبت‌نام در حال حاضر امکان‌پذیر نیست."
                    if lang == "fa"
                    else "Registration is temporarily unavailable."
                )

            else:
                password_hash = generate_password_hash(
                    form.password.data
                )

                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    display_name=display_name,
                    preferred_language=lang,
                )

                try:
                    db.session.add(user)
                    db.session.flush()

                    user_role = UserRole(
                        user_id=user.id,
                        role_id=writer_role.id,
                    )

                    db.session.add(user_role)
                    db.session.commit()

                    return redirect(
                        url_for("auth.login", lang=lang)
                    )

                except IntegrityError:
                    db.session.rollback()

                    current_app.logger.exception(
                        "Registration database integrity error"
                    )

                    form.auth_errors.append(
                        "ثبت‌نام انجام نشد. لطفاً اطلاعات خود را بررسی کرده و دوباره تلاش کنید."
                        if lang == "fa"
                        else "Registration could not be completed. Please check your information and try again."
                    )

    return render_template(
        "auth/register.html",
        lang=lang,
        form=form,
    )


@auth_bp.route("/<lang>/logout", methods=["POST"])
@login_required
def logout(lang: str) -> ResponseReturnValue:
    valid_language(lang)

    logout_user()

    return redirect(
        url_for("home", lang=lang)
    )
