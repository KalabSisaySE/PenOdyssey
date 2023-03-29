#!/usr/bin/env python3
"""the `base_model` module
defines the class `BaseModel`
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """the base class of all the other models"""

    def __init__(self, *args, **kwargs) -> None:
        """instantiates a new `BaseModel` object"""
        if kwargs:
            for key , value in kwargs.items():
                if key == "created_at":
                    self.created_at = datetime.strptime(value, "%d-%m-%Y | %H:%M:%S")
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(value, "%d-%m-%Y | %H:%M:%S")
                elif key == "__class__":
                    continue
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def save(self):
        """saves the object in the storage"""
        self.updated_at = datetime.utcnow()
        models.storage_engine.new(self)
        models.storage_engine.save()

    def to_json(self, write_to_disk: bool = False) -> dict:
        """returns the objects attributes in json format"""
        to_dict = self.__dict__.copy()
        to_dict["__class__"] = self.__class__.__name__
        if to_dict.get("_password"):
            to_dict["password"] = to_dict.get("_password")
            to_dict.pop("_password")
        for key, value in to_dict.items():
            if key == "created_at" or key == "updated_at":
                to_dict[key] = datetime.strftime(value, "%d-%m-%Y | %H:%M:%S")
        if not write_to_disk:
            to_dict.pop("password", None)
        return to_dict

    def delete(self):
        """deletes the current object from storage"""
        models.storage_engine.delete(self)
    
    def __str__(self) -> str:
        """the print/str string that is going to be printed"""
        return f"({self.__class__.__name__}): {self.id}"
        