# -*- coding: utf-8 -*-
"""
@create Time:2020-07-18

@author:LHQ
"""
from os.path import abspath, dirname, join


BASE_DIR = dirname(dirname(abspath(__file__)))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(BASE_DIR, "data.db")
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(BASE_DIR, "data.db")


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(BASE_DIR, "test_data.db")



config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
