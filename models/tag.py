#!/usr/bin/env python3
"""the `tag` module
defines the class `Tag`
"""
from models.base_model import BaseModel


class Tag(BaseModel):
    """represents the tags of a `Blog`"""
    
    tag_name = ""
    blog_id = ""
