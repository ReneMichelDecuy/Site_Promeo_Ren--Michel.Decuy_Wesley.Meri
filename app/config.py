import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://db_user:db_password@db:3306/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
