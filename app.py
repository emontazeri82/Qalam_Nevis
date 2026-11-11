import os
from dotenv import load_dotenv

from flask import Flask, abort, redirect, render_template, request, url_for

from demo_stories import DEMO_STORIES

from models.extensions import db, migrate, login_manager, csrf

from models import User
from uuid import UUID
from routes.auth import auth_bp
from flask_login import login_required, current_user

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
csrf.init_app(app)

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_uuid = UUID(user_id)
    except (ValueError, TypeError):
        return None

    return db.session.get(User, user_uuid)

@login_manager.unauthorized_handler
def unauthorized():
  lang = (request.view_args or {}).get("lang", "en")
  if lang not in ('en', 'fa'):
      abort(404)
  return redirect(url_for('auth.login', lang=lang))

    
@app.route("/")
def index():
    return redirect(url_for("home", lang="en"))


@app.route("/<lang>/")
def home(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    return render_template("home.html", lang=lang)


@app.route("/<lang>/stories/")
def stories(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    preview_articles = sorted(
        DEMO_STORIES,
        key=lambda article: (article["date"], article["slug"]),
        reverse=True,
    )

    return render_template(
        "stories.html",
        lang=lang,
        stories=preview_articles,
        total=len(preview_articles),
        demo=True,
    )

@app.route("/<lang>/reports/")
def reports(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    preview_articles = sorted(
        DEMO_STORIES,
        key=lambda article: (article["date"], article["slug"]),
        reverse=True,
    )

    return render_template(
        "reports.html",
        lang=lang,
        reports=preview_articles,
        demo=True,
    )


@app.route("/<lang>/criticism/")
def criticism(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    preview_articles = sorted(
        DEMO_STORIES,
        key=lambda article: (article["date"], article["slug"]),
        reverse=True,
    )

    return render_template(
        "criticism.html",
        lang=lang,
        criticism_articles=preview_articles,
        demo=True,
    )


@app.route("/<lang>/archive/")
def archive(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    preview_articles = sorted(
        DEMO_STORIES,
        key=lambda article: (article["date"], article["slug"]),
        reverse=True,
    )

    return render_template(
        "archive.html",
        lang=lang,
        archive_articles=preview_articles,
        demo=True,
    )


@app.route("/<lang>/articles/<slug>/")
def article_detail(lang: str, slug: str):
    if lang not in ("en", "fa"):
        abort(404)

    article = next(
        (item for item in DEMO_STORIES if item["slug"] == slug),
        None,
    )

    if article is None:
        abort(404)

    section = request.args.get("section", "stories")

    if section not in ("stories", "poetry", "reports", "criticism", "archive"):
        abort(400)

    return render_template(
        "article_detail.html",
        lang=lang,
        article=article,
        section=section,
        demo=True,
    )
@app.route("/<lang>/poetry/")
def poetry(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    preview_articles = sorted(
        DEMO_STORIES,
        key=lambda article: (article["date"], article["slug"]),
        reverse=True,
    )

    return render_template(
        "poetry.html",
        lang=lang,
        poetry_articles=preview_articles,
        total=len(preview_articles),
        demo=True,
    )


@app.route("/<lang>/writer/")
@login_required
def writer_dashboard(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    role_codes = {
        user_role.role.code
        for user_role in current_user.user_roles
    }

    if "writer" not in role_codes and "admin" not in role_codes:
        abort(403)

    return render_template(
        "writer/dashboard.html",
        lang=lang,
    )


@app.route("/<lang>/writer/articles/new")
@login_required
def writer_new_article(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    role_codes = {
        user_role.role.code
        for user_role in current_user.user_roles
    }
    if "writer" not in role_codes and "admin" not in role_codes:
        abort(403)

    return render_template(
        "writer/article_editor.html",
        lang=lang,
    )



@app.route("/<lang>/admin/")
@login_required
def admin_dashboard(lang: str):
    if lang not in ("en", "fa"):
        abort(404)

    role_codes = {
        user_role.role.code
        for user_role in current_user.user_roles
    }

    if not role_codes.intersection({"admin", "editor"}):
        abort(403)

    return render_template(
        "admin/dashboard.html",
        lang=lang,
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1", 
        port=5001,
        debug=False
    )
