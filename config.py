"""This module is to configure app to connect with database."""

from pymongo import MongoClient

DATABASE = MongoClient()['UsersData'] # DB_NAME
DB_NAME = "UsersData"
DEBUG = True
client = MongoClient('localhost', 27017)