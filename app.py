
from flask import Flask, render_template, url_for, redirect, request, session
import os

PORT = os.getenv('PORT', 5000)

app = Flask(__name__)

# Main page
@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("home.html")


# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True
    app.run(port=PORT)