#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form = """
<form method="post">
	<label>Username<input type="text" name="username" value="%(username)s"></label>
	<br>
	<label>Password<input type="password" name="password"></label>
	<br>
	<label>Verify Password<input type="password" name="verify"></label>
	<br>
	<label>Email (optional)<input type="text" name="email" value="%(email)s"></label>
	<br>
	<label>%(error)s</label>
	<br>
	<input type="submit">
</form>
"""
welcome = """
Welcome, %(username)s!
"""
user_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
password_re = re.compile("^.{3,20}$")
email_re = re.compile("^[\S]+@[\S]+\.[\S]+$")

class MainHandler(webapp2.RequestHandler):
	def escape(self, input):
		for (i,o) in (("&", "&amp;"),
					  (">", "&gt;"),
					  ("<", "&lt;"),
					  ('"', "&quot;")):
			input = input.replace(i, o)
			return input
	
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		valid = True
		error = None
		if user_re.match(username) == None:
			valid = False
			error = "User name is invalid"
		elif password_re.match(password) == None:
			valid = False
			error = "Password is invalid"
		elif password != verify:
			valid = False
			error = "Passwords do not match"
		elif email and email_re.match(email) == None:
			valid = False
			error = "Email entered is invalid"

		if valid:
			self.redirect("/welcome?username=%(username)s" % {"username" : self.escape(username)})
		else:
			self.response.out.write(form % {"username" : self.escape(username),
											"email" : self.escape(email),
											"error" : error})

	def get(self):
		self.response.out.write(form % {"username" : "", 
										"email" : "", 
										"error" : ""})
		

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		self.response.out.write(welcome % {"username" : username})

app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/welcome', WelcomeHandler)],
                              debug=True)
