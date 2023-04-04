#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Flask web application.
"""


import io
import json
import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

import config
import helper
import visualize


# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "123bnfsdbjfyusdf67vcnjakdhs"
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER


@app.route("/")
@app.route("/home")
def index():
    """Homepage of the dashboard."""

    # Construct the path to the graph JSON file
    data_path = helper.get_graph_json_path()
    # Determine if the graph JSON file exists at that path
    data_exists = os.path.isfile(data_path)

    # If the graph json exists, read the data
    if data_exists:
        with open(data_path, "r") as graph_data:
            graph_json = graph_data.read()
    else:
        graph_json = None
    
    # Render the page given the following variables
    return render_template(
        "index.html",
        valid_extensions=config.VALID_EXTENSIONS,
        graph=graph_json,
    )


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
            visualize.graphjson_from_df(
                df,
                output_path=helper.get_graph_json_path(),
            )
    
    # Redirect to the homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    helper.create_upload_folder()
    app.run(debug=True)