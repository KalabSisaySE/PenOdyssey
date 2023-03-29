#!/usr/bin/env python3
"""initialize blueprint views"""

from flask import Blueprint

pen_ody = Blueprint("pen_ody", __name__, url_prefix="/api/v1")

from api.v1.views.blogs import *
from api.v1.views.bookmarks import *
from api.v1.views.categories import *
from api.v1.views.comments import *
from api.v1.views.likes import *
from api.v1.views.subscriptions import *
from api.v1.views.tags import *
from api.v1.views.users import *
from api.v1.views.blog_categories import *
from api.v1.views.categories import *


from api.v1.views.index import *