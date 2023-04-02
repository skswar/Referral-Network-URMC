import io
import json
import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import helper
import visualize


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
        secure_filename("graph.json")               # filename
    )
    data_exists = os.path.isfile(data_path)

    if data_exists:
        with open(data_path, "r") as graph_data:
            graph_json = graph_data.read()
    else:
        graph_json = None
    
    return render_template("index.html", graph=graph_json)


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
            # TODO: Check if format is correct
            ...

            # Read file into dataframe in memory
            data_string = str(file_to_upload.read(), "utf-8")
            data_stream = io.StringIO(data_string)
            df = pd.read_csv(data_stream)

            # Create and save the visualization
            visualize.graphjson_from_df(df, output_path=os.path.join(
                os.path.abspath(os.path.dirname(__file__)), # project directory
                app.config["UPLOAD_FOLDER"],                # upload directory
                secure_filename("graph.json")               # filename
            ))
    
    # Redirect to the homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)