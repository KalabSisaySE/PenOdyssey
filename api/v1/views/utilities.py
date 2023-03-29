#!/usr/bin/enc python3
"""the `utilities` module
defines some utility functions for the view modules
"""
from typing import TypeVar, List
from models import storage_engine

host = "http://127.0.0.1:5000/api/v1/"


def fetch_blog_data(model: str, blog: TypeVar("Blog")) -> List:
    """fetches the blog_id for the requested model
    that contains the `blog_id`"""
    if model == "BlogCategory":
        prefix = host + model.lower() + "/"
    else:
        prefix = host + model.lower() + "s/"
    fetched_data = list(filter(lambda x:x.blog_id == blog.id ,storage_engine.all(model=model)))
    if len(fetched_data) > 0:
        return [prefix + data.id for data in fetched_data]
    else:
        return []
    
def fetch_user_data(model: str, user: TypeVar("User")) -> List:
    """fetched the database for the requested model
    that contains the `user_id`"""
    prefix = host + model.lower() + "s/"
    if model != "Subscription":
        fetched_data = list(filter(lambda x:x.user_id == user.id ,storage_engine.all(model=model)))
        if len(fetched_data) > 0:
            return [prefix + data.id for data in fetched_data]
        else:
            return []
    else:
        subscription = []
        for attr in ["subscriber_id","writer_id"]:
            fetched_data = list(filter(lambda x:getattr(x, attr) == user.id ,storage_engine.all(model=model)))
            if len(fetched_data) > 0:
                subscription.append({
                    attr: [prefix + data.id for data in fetched_data]
                })
            else:
                subscription.append({})
        return subscription
    