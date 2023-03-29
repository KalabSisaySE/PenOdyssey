#!/usr/bin/env python3
"""the `like` module
defines the class `Like`
"""
from models.base_model import BaseModel


class Like(BaseModel):
    """represents the likes of a `Blog`"""
    
    user_id = ""
    blog_id = ""
