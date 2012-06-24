__author__ = 'Devin'

import BaseHandler
import User
import re

########## Registration validation ############
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

################# Handlers ##################
class UserHandler(BaseHandler.BaseHandler):
    def login(self, user):
        self.response.headers.add_header("Set-Cookie",
                                         "username=%s; Path=/" % str(User.make_secure_value(user.username)))
        self.redirect('/blog/welcome')

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "username=; Path=/")
        self.redirect('/blog/signup')

class RegisterHandler(UserHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username,
            email = email)

        matchingUser = User.User.by_name(username)
        have_error = False
        if matchingUser:
            params['error_username'] = "Username already exists"
            have_error = True

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            user = User.User.register(username=username, password=password, email=email)
            user.put()
            self.login(user)

class LoginHandler(UserHandler):
    def get(self):
        self.render('login-form.html')
        return
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = User.User.login(username, password)
        if user:
            self.login(user)
        else:
            self.render('login-form.html', error = "Invalid Login")
        return

class LogoutHandler(UserHandler):
    def get(self):
        self.logout()

class WelcomeHandler(UserHandler):
    def get(self):
        cookieValue = self.request.cookies.get('username')
        username = User.check_secure_value(cookieValue)
        if username:
            self.render('welcome.html', username = username)
        else:
            self.logout()
