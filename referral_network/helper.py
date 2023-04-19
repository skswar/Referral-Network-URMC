#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Miscellaneous helper functions for the Flask application.
"""


import os

from werkzeug.utils import secure_filename

import config


def get_logging_path() -> str:
    """Gets the filepath of the logging file."""

    outer_directory = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__))      # two levels out
    )
    return os.path.join(outer_directory, config.LOGGING_FILENAME)


def create_upload_folder() -> None:
    """Creates the `files` folder in the static directory for uploaded files."""

    if not os.path.exists(get_upload_folder_path()):
        os.makedirs(get_upload_folder_path())


def get_upload_folder_path() -> str:
    """Gets the filepath of the folder where uploaded files are stored."""

    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),     # project directory
        config.UPLOAD_FOLDER,                           # upload directory
    )


def valid_filetype(filename: str) -> bool:
    """Returns whether or not the specified file is of a valid filetype."""
    return os.path.splitext(filename)[1] in config.VALID_EXTENSIONS


def get_graph_csv_path() -> str:
    """Gets the path of the graph CSV file."""

    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),     # project directory
        config.UPLOAD_FOLDER,                           # upload directory
        secure_filename(config.GRAPH_CSV_FILENAME)     # filename
    )

def get_graph_json_path() -> str:
    """Gets the path of the graph JSON file."""

    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),     # project directory
        config.UPLOAD_FOLDER,                           # upload directory
        secure_filename(config.GRAPH_JSON_FILENAME)     # filename
    )