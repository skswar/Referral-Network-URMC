#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Miscellaneous helper functions for the Flask application.
"""


import os

from werkzeug.utils import secure_filename

import config


def valid_filetype(filename: str) -> bool:
    """Returns whether or not the specified file is of a valid filetype."""
    return os.path.splitext(filename)[1] in config.VALID_EXTENSIONS


def get_graph_json_path() -> str:
    """Gets the path of the graph JSON file."""

    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),     # project directory
        config.UPLOAD_FOLDER,                           # upload directory
        secure_filename(config.GRAPH_JSON_FILENAME)     # filename
    )