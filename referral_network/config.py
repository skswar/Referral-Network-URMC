#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration variables for the Flask application.
"""


from typing import Final

UPLOAD_FOLDER: Final = "static/files"

VALID_EXTENSIONS: Final = {
    ".csv",
}

GRAPH_JSON_FILENAME: Final = "graph.json"