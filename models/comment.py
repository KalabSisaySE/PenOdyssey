#!/usr/bin/env python3
"""the `comment` module
defines the class `Comment`
"""
from models.base_model import BaseModel


class Comment(BaseModel):
    """represents the comments in a `Blog`"""

    user_comment = ""
    user_id = ""
    blog_id = ""