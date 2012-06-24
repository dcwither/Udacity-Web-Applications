__author__ = 'Devin'

import random
import hashlib
import string
import hmac
from google.appengine.ext import db

########## Salting, Password Hash ############
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return make_pw_hash(name, pw, salt) == h

########## User Cookies ############

secret = "super secret"

def make_secure_value(value):
    return '%s|%s' % (value, hmac.new(secret, value).hexdigest())

def check_secure_value(secure):
    value = secure.split('|')[0]
    if secure == make_secure_value(value):
        return value
    else:
        return None

############## User Object ################
def user_key(name='default'):
    return db.Key.from_path('users', name)

class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = user_key())

    @classmethod
    def by_name(cls, username):
        u = User.all().filter('username =', username).get()
        return u

    @classmethod
    def register(cls, username, password, email = None):
        pw_hash = make_pw_hash(username, password)
        return User(parent = user_key(),
            username = username,
            pw_hash = pw_hash,
            email = email)

    @classmethod
    def login(cls, username, password):
        user = cls.by_name(username)
        if user and valid_pw(username, password, user.pw_hash):
            return user

