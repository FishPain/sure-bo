from flask import Flask, render_template, request
from src.ml.inference_worker import InferenceWorker
import os

PORT = int(os.getenv('PORT', 5001))

from src.app import app_utils

app = Flask(__name__)

# Main page
@app.route("/", methods=["GET", "POST"])
def root():
    job_dict, pred_bool, exp_list, raw_text = None, None, None, None

    if request.method == "POST":
        if request.form.get("mock_inference"):
            job_dict = app_utils.get_mock_job()
        else:
            url = request.form.get("job_street_url")
            if not app_utils.is_valid_jobstreet_url(url):
                return render_template("home.html", url_error=True)
            try:
                job_dict = app_utils.get_job_from_jobstreet(url)
            except Exception as e:
                return render_template("home.html", scrape_error_msg=e)
        try:
            pred = InferenceWorker(job_dict)
            pred_bool = True if int(pred.predict()[0]) == 1 else False
            exp_list = pred.explain()[0]
            raw_text = pred.raw_text
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template("home.html", pred_error_msg=e)
                
    return render_template("home.html", job_dict=job_dict, pred_bool=pred_bool, exp_list=exp_list, raw_text=raw_text)


# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=PORT)
