#!/usr/bin/env python3
"""the `blog_category` module
defines the class `BlogCategory`
"""
from models.base_model import BaseModel


class BlogCategory(BaseModel):
    """represents the relation between a `Blog` and a `Category`"""

    blog_id = ""
    category_id = ""
