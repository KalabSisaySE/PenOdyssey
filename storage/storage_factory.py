#!/usr/bin/env python3
"""the `storage_factory` module"""


def get_file_storage():
    """returns a `file_storage` object"""
    from .file_storage import FileStorage
    return FileStorage()

def get_db_storage():
    """returns a `db_storage` object"""
    from .db_storage import DbStorage
    return DbStorage()
