#!/usr/bin/env python
import datetime
import json
from flask import Flask, redirect, request, session, render_template

from ldaploginprovider import LDAPLoginProvider

class Config:
    flask_secret_key = 'e5ac358c-f0bf-11e5-9e39-d3b532c10fff'
    # ldap_server = ''
    # ldap_user_prefix = "MYDOMAIN\\"
    # ldap_base_dn = "DC=XXX,DC=XX"
    # known_user = 'JoeTestUser'
    # known_pass = 'JoePassword'

app = Flask(__name__)
app.config['CONFIG'] = Config()
app.config['SECRET_KEY'] = app.config['CONFIG'].flask_secret_key

@app.route("/")
def controller_default():
    if not session.get('username'):
        return redirect('/login')

    username = session.get('username', None)
    displayname = session.get('displayname', None)
    return render_template('index.html', username=username, displayname=displayname)

@app.route("/login", methods=["GET"])
def controller_login():
    msg = ""
    print session
    if session.get('err'):
        msg = session.get('err')
        del session['err']

    return render_template('login.html', msg=msg)

@app.route("/process-login", methods=["GET"])
def controller_login_get():
    return redirect("/")

@app.route("/process-login", methods=["POST"])
def controller_login_post():
    config = app.config['CONFIG']
    ldap_provider = LDAPLoginProvider(config.ldap_server, config.ldap_base_dn, config.ldap_user_prefix)
    ldap_provider.build_connection()

    username = request.form.get('username', None)
    password = request.form.get('password', None)

    app.logger.info("Attempting login for: " + str({'username': username, 'password': password}))

    if username and password:
        user = ldap_provider.login(username, password)
        session['username'] = username
        session['displayname'] = user.displayName
        session['logged_in'] = True

    else:
        session['err'] = "INVALID_CREDENTIALS"

    return redirect('/')

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
