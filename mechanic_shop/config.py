import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:<YOUR MYSQL PASSWORD>@localhost/mechanic_shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    JWT_EXPIRATION_TIME = 3600  