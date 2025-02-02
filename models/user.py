#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """Getter attribute"""
        if models.storage_t == 'db':
            return self.__dict__.get('password', None)
        return self.__dict__.get('password', "")

    @password.setter
    def password(self, password):
        """Hashes the password"""
        p_w = md5(bytes(password.encode('utf-8'))).hexdigest()
        self.__dict__['password'] = p_w

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            p_word = kwargs.pop('password', None)
            if p_word:
                self.password = p_word
        super().__init__(*args, **kwargs)
