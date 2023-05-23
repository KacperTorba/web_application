import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DIR = 'sqlite:///' + os.path.join(BASE_DIR ,'app','data')

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY")  
   SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or os.path.join(SQLITE_DIR ,'user.db'))
   SECURITY_PASSWORD_SALT = (os.environ.get("SECURITY_PASSWORD_SALT"))
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   MAIL_SERVER = 'smtp.gmail.com'  # Flask mail
   MAIL_PORT = 465
   MAIL_USE_SSL = True
   MAIL_USERNAME = 'infokactor@gmail.com'  
   MAIL_PASSWORD = 'tmpqlpctjqebaste'

   
