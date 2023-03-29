#!/usr/bin/env python3
"""the `file_storage` module
handles data storage in files"""
import bcrypt
import json
from typing import List
from os import path
from models.blog import Blog
from models.blog_category import BlogCategory
from models.bookmark import Bookmark
from models.category import Category
from models.comment import Comment
from models.like import Like
from models.subscription import Subscription
from models.tag import Tag
from models.user import User


class FileStorage:
    """json file storage"""
    _file_path = "files.json"
    _objects = {}
    _models = {
        "Blog": Blog,
        "BlogCategory": BlogCategory,
        "Bookmark": Bookmark,
        "Category": Category,
        "Comment": Comment,
        "Like": Like,
        "Subscription": Subscription,
        "Tag": Tag,
        "User": User
    }

    def all(self, model=None) -> List: 
        """returns all the objects in a class if `model` is specified
        otherwise returns all objects from all classes. model can
        be a string(class name) or the class itself"""
        if model:
            if model in self._models.values():
                model_name = model.__name__
            elif type(model) is str:
                model_name = model
            objs = self._objects.get(model_name)
            if objs:
                return list(objs.values())
            else:
                return []
        return self._objects

    def new(self, obj):
        """add a new obj to `objects`"""
        if obj:
            if isinstance(obj, tuple(self._models.values())):
                model_name = obj.__class__.__name__
                if self._objects.get(model_name):
                    self._objects[model_name].update({obj.id: obj})
                else:
                    if model_name in self._models:
                        self._objects[model_name] = {obj.id: obj}

    def save(self):
        """save all the objects stored in `objects` to file"""
        to_file = {}
        # serialize all objects to json
        for model in self._objects:
            to_file[model] = {}
            for key, obj in self._objects[model].items():
                json_data = obj.to_json(write_to_disk=True)
                to_file[model][key] = json_data
        # write to file
        with open(self._file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(to_file))

    def reload(self):
        """reload all objects saved on file to `objects`"""
        if path.exists(self._file_path):
            with open(self._file_path, "r") as f:
                file = json.loads(f.read())
                to_objects = {}
                # convert json back to object
                for model in file:
                    to_objects[model] = {}
                    for model_id, data in file[model].items():
                        if model == "User": 
                            model_data = data.copy()
                            model_data["_password"] = model_data["password"]
                            model_data.pop("password", None)
                        else:
                            model_data = data.copy()

                        obj = eval(model)(**model_data)
                        to_objects[model][model_id] = obj

                self._objects = to_objects

    def delete(self, obj):
        """deletes the given `obj` from objects and file"""
        model_name = obj.__class__.__name__
        if self._objects.get(model_name):
            self._objects[model_name].pop(obj.id, None)
        self.save()
    
    def close(self):
        """reloads"""
        self.reload()
    
    def get(self, model, id):
        """returns the object with the given `model` and `id`
        `model` can be a string or a class"""
        if model:
            if model in self._models.values():
                model_name = model.__name__
            if type(model) is str:
                model_name = model
            if model_name in self._objects:
                return self._objects[model_name].get(id)
    
    def count(self, model=None) -> int:
        """counts the number of object of the given type if model is given
        otherwise returns the total number of objects"""
        data = self.all(model=model)
        if data:
            return len(data)
