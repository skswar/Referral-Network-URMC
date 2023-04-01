import os

import config


def valid_filetype(filename: str) -> bool:
    """"""
    return os.path.splitext(filename)[1][1:] in config.VALID_EXTENSIONS