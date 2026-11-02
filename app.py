from flask import Flask
from views import (
  index, home, stories, 
  login, register, reports, 
  criticism, archive, article_detail,
  writer_dashboard, writer_new_article,
)
app = Flask(__name__)

app.add_url_rule(
    "/",
    endpoint="index",
    view_func=index,
)
app.add_url_rule(
  "/<lang>/",
  endpoint="home",
  view_func=home,
)
app.add_url_rule(
  "/<lang>/stories/",
  endpoint="stories",
  view_func=stories,
)
app.add_url_rule(
  "/<lang>/login",
  endpoint="login",
  view_func=login,
)
app.add_url_rule(
  "/<lang>/register",
  endpoint="register",
  view_func=register,
)
app.add_url_rule(
  "/<lang>/reports/",
  endpoint="reports",
  view_func=reports,
)
app.add_url_rule(
  "/<lang>/criticism/",
  endpoint="criticism",
  view_func=criticism,
)
app.add_url_rule(
  "/<lang>/archive/",
  endpoint="archive",
  view_func=archive,
)
app.add_url_rule(
  "/<lang>/articles/<slug>/",
  endpoint="article_detail",
  view_func=article_detail,
)
app.add_url_rule(
    "/<lang>/writer/",
    endpoint="writer_dashboard",
    view_func=writer_dashboard,
)
app.add_url_rule(
  "/<lang>/writer/articles/new",
  endpoint="writer_new_article",
  view_func=writer_new_article,
)

if __name__ == "__main__":
  app.run(debug=True, port=5001)