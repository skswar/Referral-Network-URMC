#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Flask web application.
"""


import argparse
import logging
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
        app.logger.info(f"Data file exists at: {data_path}")
        with open(data_path, "r") as graph_data:
            graph_json = graph_data.read()
    else:
        app.logger.info(f"Data file does not exist at: {data_path}")
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
            app.logger.info("CSV file was uploaded")

            # Save the file to disk for easy access
            file_to_upload.save(helper.get_graph_csv_path())

            # Read file into dataframe
            df = pd.read_csv(helper.get_graph_csv_path())

            # Create and save the visualization
            app.logger.info("Creating visualization from uploaded file")
            visualize.graphjson_from_df(
                df,
                output_path=helper.get_graph_json_path(),
            )
            app.logger.info(
                f"Graph JSON file saved at: {helper.get_graph_json_path()}"
            )
    
    # Redirect to the homepage
    return redirect(url_for("index"))


@app.route("/modify", methods=["GET", "POST"])
def modify():
    """Modifies an existing visualization via POST method.
    
    Redirects the user back to the homepage if accessed by URL.
    """

    # Check if the request was posted by the form on the homepage
    if request.method == "POST" and os.path.exists(helper.get_graph_csv_path()):
        app.logger.info("Visualization modification requested")

        # Read the values on the form
        minimum_referrals = request.form.get("min-referrals")
        app.logger.info(f"Setting minimum referrals: {minimum_referrals}")

        department_filter = request.form.get("department-filter")
        app.logger.info(f"Setting department: {department_filter}")

        node_pair_efficiency = request.form.get("node-pair-efficiency")
        app.logger.info(f"Setting node pair efficiency: {node_pair_efficiency}")

        degree_filter = request.form.get("degree-filter")
        app.logger.info(f"Setting degree directionality: {degree_filter}")

        # Read file into dataframe
        df = pd.read_csv(helper.get_graph_csv_path())

        # Create and save the visualization
        app.logger.info("Modifying visualization from uploaded file")
        visualize.graphjson_from_df(
            df,
            output_path=helper.get_graph_json_path(),
            minimum_referrals=int(minimum_referrals),
            department_filter=department_filter,
            node_pair_efficiency=float(node_pair_efficiency),
            degree_filter=degree_filter,
        )
        app.logger.info(
            f"Graph JSON file saved at: {helper.get_graph_json_path()}"
        )

    # Redirect to the homepage
    return redirect(url_for("index"))


if __name__ == "__main__":

    # Initialize the command line argument parser
    parser = argparse.ArgumentParser()

    # Allow the user to specify whether or not to run in debug mode
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help=(
            "Whether or not to run the Flask application in debug mode."
        ),
    )

    # Parse the arguments
    args = parser.parse_args()

    # Create the upload folder if necessary
    helper.create_upload_folder()

    # Log warnings and above to file if not in debug mode
    if not args.debug:
        logging.basicConfig(
            filename=helper.get_logging_path(), level=logging.WARNING
        )

    # Run the Flask application
    app.run(debug=args.debug)