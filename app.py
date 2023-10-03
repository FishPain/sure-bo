from flask import Flask, render_template, url_for, redirect, request, session
from src.ml.inference_worker import InferenceWorker, SMOTETomekTransformer
import os

PORT = os.getenv('PORT', 5000)

from src.app import app_utils

app = Flask(__name__)


# Main page
@app.route("/", methods=["GET", "POST"])
def root():
    job_dict = None
    pred_bool = None
    exp_list = None
    if request.method == "POST":
        url = request.form["job_street_url"]
        if app_utils.is_valid_jobstreet_url(url):
            job_dict = app_utils.get_job_from_jobstreet(url)
            if job_dict:
                # Use try-except to handle exceptions during prediction
                pred = InferenceWorker(job_dict)
                pred_bool = True if int(pred.predict()[0]) == 1 else False
                exp_list = pred.explain()
        else:
            return render_template("home.html", url_error=True)
    return render_template("home.html", job_dict=job_dict, pred_bool=pred_bool, exp_list=exp_list)


# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.debug = True
    app.run(port=PORT)
