from flask import Flask, abort, redirect, render_template, request, url_for

from demo_stories import DEMO_STORIES

app = Flask(__name__)


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

    # Accept only known listing endpoints for the back link.
    section = request.args.get("section", "stories")

    if section not in ("stories", "reports", "criticism", "archive"):
        abort(400)

    return render_template(
        "article_detail.html",
        lang=lang,
        article=article,
        section=section,
        demo=True,
    )
@app.route("/<lang>/login")
def login(lang):
    return render_template("auth/login.html", lang=lang)


@app.route("/<lang>/register")
def register(lang):
    return render_template("auth/register.html", lang=lang)

if __name__ == "__main__":
    app.run(debug=True)