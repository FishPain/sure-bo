from flask import Flask, render_template, url_for, redirect, request, session
from src.app import app_utils, constants

app = Flask(__name__)


# Main page
@app.route("/", methods=["GET", "POST"])
def root():
    job_dict = None
    if request.method == "POST":
        url = request.form["job_street_url"]
        if app_utils.is_valid_jobstreet_url(url):
            job_dict = app_utils.get_job_from_jobstreet(url)
        else:
            return render_template("home.html", url_error=True)
    return render_template("home.html", job_dict=job_dict)


# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.debug = True
    app.run()
