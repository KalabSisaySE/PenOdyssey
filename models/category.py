#!/usr/bin/env python3
"""the `category` module
defines the class `Category`
"""
from models.base_model import BaseModel


class Category(BaseModel):
    """represents a category that a `Blog` belongs to"""

    category_name = ""
    category_description = ""