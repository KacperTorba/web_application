import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DIR = 'sqlite:///' + os.path.join(BASE_DIR ,'app','data')

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY")  
   SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or os.path.join(SQLITE_DIR ,'user.db'))
   print(SQLALCHEMY_DATABASE_URI)
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   
