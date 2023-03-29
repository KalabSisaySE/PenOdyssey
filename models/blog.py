#!/usr/bin/env python3
"""the `blog` module
defines the class `Blog`
"""
from models.base_model import BaseModel


class Blog(BaseModel):
    """represents a `Blog`"""

    blog_title = ""
    blog_content = ""
    user_id = ""

    def __str__(self) -> str:
        """returns the string representation of the object"""
        return f"(Blog): {self.blog_title}"