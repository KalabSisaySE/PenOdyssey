#!/usr/bin/env python3
"""the `subscription` module
defines the class `Subscription`
"""
from models.base_model import BaseModel


class Subscription(BaseModel):
    """represents the subscribers of a `User`"""

    subscriber_id = ""
    writer_id = ""
