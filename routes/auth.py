from flask import Blueprint, abort, render_template, redirect, url_for
from forms.auth import LoginForm, RegisterForm
from werkzeug.security import (
  generate_password_hash,
  check_password_hash,
)
from sqlalchemy import select,  func
from models.extensions import db

from sqlalchemy.exc import IntegrityError
from flask.typing import ResponseReturnValue

from flask_login import login_user, logout_user, login_required

from models import User, Role, UserRole

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/<lang>/login", methods=["GET", "POST"])
def login(lang: str) -> ResponseReturnValue:
    if lang not in ("en", "fa"):
        abort(404)

    form = LoginForm(lang=lang)
    if form.validate_on_submit():
        username = form.username.data.strip()

        stmt = select(User).where(
            func.lower(User.username) == username.lower()
        )
        user = db.session.scalar(stmt)
        if user is None:
            message = (
                "نام کاربری یا رمز عبور اشتباه است."
                if lang == "fa"
                else "Invalid username or password."
            )
            form.form_errors.append(message)
        else:
            password = form.password.data
            password_valid = check_password_hash(
                user.password_hash,
                password
            )
            if not password_valid or not user.is_active:
                message = (
                    "نام کاربری یا رمز عبور اشتباه است."
                    if lang == "fa"
                    else "Invalid username or password."
                )
                form.form_errors.append(message)
            else:
                role_codes = {
                    user_role.role.code
                    for user_role in user.user_roles
                }

                if "admin" in role_codes or "editor" in role_codes:
                    login_user(user, remember=bool(form.remember.data))
                    return redirect(url_for("admin_dashboard", lang=lang))

                elif "writer" in role_codes:
                    login_user(user, remember=bool(form.remember.data))
                    return redirect(url_for("writer_dashboard", lang=lang))

                else:
                    form.form_errors.append(
                        "حساب شما مجوز دسترسی ندارد."
                        if lang == "fa"
                        else "Your account does not have an assigned access role."
                    )
                
    
    return render_template(
        "auth/login.html", 
        lang=lang,
        form=form
    )


@auth_bp.route("/<lang>/register", methods=["GET", "POST"])
def register(lang: str) -> ResponseReturnValue:
    if lang not in ("en", "fa"):
        abort(404)

    form = RegisterForm(lang=lang)

    if form.validate_on_submit():
        
        username = form.username.data.strip()
        username_stmt = select(User).where(
            func.lower(User.username) == username.lower()
        )
        existing_user = db.session.scalar(username_stmt)
        if existing_user is not None:
            message = (
                "این نام کاربری قبلاً ثبت شده است."
                if lang == "fa"
                else "This username is already taken."
            )
            form.username.errors.append(message)

        email = form.email.data.strip()
        email_stmt = select(User).where(
            func.lower(User.email) == email.lower()
        )
        existing_email = db.session.scalar(email_stmt)
        if existing_email is not None:
            message = (
                "این ایمیل قبلاً ثبت شده است."
                if lang == "fa"
                else "This email is already taken."
            )
            form.email.errors.append(message)
        if not form.username.errors and not form.email.errors:
            writer_stmt = select(Role).where(
                Role.code == "writer"
            )
            writer_role = db.session.scalar(writer_stmt)
            if writer_role is None:
                form.form_errors.append(
                    "ثبت‌نام در حال حاضر امکان‌پذیر نیست."
                    if lang == "fa"
                    else "Registration is temporarily unavailable."
                )
            else:
                # Continue creating the user
                password_hash = generate_password_hash(form.password.data)
                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    display_name=form.name.data,
                    preferred_language=lang
                )
                try:
                    db.session.add(user)
                    db.session.flush()

                    user_role = UserRole(
                        user_id=user.id,
                        role_id=writer_role.id
                    )

                    db.session.add(user_role)
                    db.session.commit()
                    return redirect(url_for("auth.login", lang=lang))
                except IntegrityError:
                    db.session.rollback()

                    message = (
                        "ثبت‌نام انجام نشد. لطفاً اطلاعات خود را بررسی کرده و دوباره تلاش کنید."
                        if lang == "fa"
                        else "Registration could not be completed. Please check your information and try again."
                    )

                    form.form_errors.append(message)

    return render_template(
        "auth/register.html", 
        lang=lang,
        form=form
    )
@auth_bp.route("/<lang>/logout", methods=["POST"])
@login_required
def logout(lang: str) -> ResponseReturnValue:
    if lang not in ("en", "fa"):
        abort(404)

    logout_user()
    return redirect(url_for('home', lang=lang))
