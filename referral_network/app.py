import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import helper


# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "123bnfsdbjfyusdf67vcnjakdhs"
app.config["UPLOAD_FOLDER"] = "static/files"


@app.route("/")
@app.route("/home")
def index():
    """Homepage of the dashboard."""

    data_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), # project directory
        app.config["UPLOAD_FOLDER"],                # upload directory
        secure_filename("data.csv")                 # filename
    )
    data_exists = os.path.isfile(data_path)

    df = pd.read_csv(data_path) if data_exists else None
    df_html = df.head().to_html(index=False) if data_exists else None

    return render_template("index.html", data_exists=data_exists, df=df_html)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Uploads a file via POST method.
    
    Redirects the user back to the homepage if accessed by URL.
    """

    # Check if the request was posted by the form on the homepage
    if request.method == "POST":
        # Get the requested file
        file_to_upload = request.files["uploadFile"]
        # Check if the file exists and is a valid filetype
        if file_to_upload and helper.valid_filetype(file_to_upload.filename):
            # Save the file
            file_to_upload.save(os.path.join(
                os.path.abspath(os.path.dirname(__file__)), # project directory
                app.config["UPLOAD_FOLDER"],                # upload directory
                secure_filename("data.csv")                 # filename
            ))
    
    # Redirect to the homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)