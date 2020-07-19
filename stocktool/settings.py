# -*- coding: utf-8 -*-
"""
@create Time:2020-07-18

@author:LHQ
"""
from os.path import abspath, dirname, join


BASE_DIR = abspath(dirname(dirname(__name__)))



class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(BASE_DIR, "data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
