from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask import request
from wtforms import BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, InputRequired,EqualTo
from datetime import datetime
import hashlib
import binascii
from urllib.parse import urlparse, urljoin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default= 0)
    reg_date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return ('User: {},{}'.format(self.id, self.mail))

    def get_hashed_password(password):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(stored_password_hash, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password_hash[:64]
        stored_password = stored_password_hash[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'),  100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    

class LoginForm(FlaskForm):
    mail = EmailField('E-mail',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')

class NewUserByAdmin(FlaskForm):
    mail = EmailField('E-mail',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()], default='0000')
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    is_admin = BooleanField('Is Admin')
    
    
class Registration(FlaskForm):
    mail = EmailField('E-mail',validators=[DataRequired(),Email()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField ('Repeat Password')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
