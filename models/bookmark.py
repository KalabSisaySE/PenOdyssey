#!/usr/bin/env python3
"""the `bookmark` module
defines the class `Bookmark`
"""
from models.base_model import BaseModel


class Bookmark(BaseModel):
    """represents bookmarks of a `User`"""

    blog_id = ""
    user_id = ""