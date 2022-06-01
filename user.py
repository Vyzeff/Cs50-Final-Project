from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

from models import models, CreateUser, GetUser

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")


success = False
def register(method):
    """
    will ask for an unused username
    will ask for a password ate least 8 digits long, together with 1 number and 1 symbol
    maybe implement captcha???
    must have invalid when input user already exists in db
    """
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("register.html", invalid="1")
        if not request.form.get("password"):
            return render_template("register.html", invalid="2")
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("register.html", invalid="3")
        
        # lowercase username for consistensy
        userLow = request.form.get("username").lower()
        # username is already in use

        if GetUser(userLow, 2) != 0:
            return render_template("register.html", invalid="4")
        
        # Hash password with sha256 and salt 8
        passHash = generate_password_hash(request.form.get("password"), "sha256", 8)
        
        # create a new user with the input values
        CreateUser(userLow, passHash)
        success = True
        return render_template("login.html", success=1)

    return render_template("register.html")

def login(): 
    """    
    will redirect to login page
    will take a username and password
    check if those things are in db
    either log in or error popup
    Forgets user
    when user and/or password go wrong, reload with invalid for html if
    """
    # forgets previous session
    session.clear()
    
    
    if request.method == "GET":
        if success == True:
            success == False
            return render_template("login.html", success="1")
        return render_template("login.html")
    
    #these will only happen if the method is post
    if not request.form.get("username"):
            return render_template("login.html", invalid="1")
    if not request.form.get("password"):
        return render_template("login.html", invalid="1")
    
    # query in sql in the user table where username = input in username, grab first
    # returns a dict
    
    userInput = GetUser(request.form.get("username").lower(), 1)
    
    # check if there was a username like that and if the password is correct by the hash
    if userInput == None or not check_password_hash(userInput.hash, request.form.get("password")):
        return render_template("login.html", invalid="1")
    # remember the user id
    session["user_id"] = userInput.id
    
    return redirect("/")

def logout():
    """
    forgets user id and 'logs out'
    """
    session.clear()
    
    return redirect("/")