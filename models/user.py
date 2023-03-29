#!/usr/bin/env python3
"""the `user` module
defines the class `User`
"""
import bcrypt
from flask_login import UserMixin
from models.base_model import BaseModel


class User(BaseModel, UserMixin):
    """represents the user"""

    first_name = ""
    last_name = ""
    email = ""
    bio = ""
    interests = ""
    _password = ""
    
    @property
    def password(self):
        """password getter"""
        return self._password
    
    @password.setter
    def password(self, password: str):
        """password setter"""
        if password and type(password) is str:
            pass_byte = password.encode("utf-8")
            self._password = bcrypt.hashpw(pass_byte, bcrypt.gensalt()).decode("utf-8")

    def __str__(self) -> str:
        """returns the str/print representation"""
        return f"{self.__class__.__name__}: {self.first_name} {self.last_name}"