from flask import Blueprint, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash

from models import CreateUser, GetUser

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")


success = False
def register(user, password):
    """
    will ask for an unused username
    will ask for a password at least 8 digits long, together with 1 number and 1 symbol
    must have invalid when input user already exists in db
    """
    # lowercase username for consistensy
    userLow = str(user).lower()
    # username is already in use

    if GetUser(userLow, 2) != 0:
        return render_template("register.html", invalid="4")
    
    # Hash password with sha256 and salt 8
    passHash = generate_password_hash(password, "sha256", 8)
    
    # create a new user with the input values
    CreateUser(userLow, passHash)

def login(user, password): 
    """    
    will redirect to login page
    will take a username and password
    check if those things are in db
    either log in or error popup
    Forgets user
    when user and/or password go wrong, reload with invalid for html if
    """
     
    userInput = GetUser(str(user).lower(), 1)
    
    # check if there was a username like that and if the password is correct by the hash
    if userInput == None or not check_password_hash(userInput.hash, password):
        return False
    # remember the user id
    session["user_id"] = userInput.id
    
def logout():
    """
    forgets user id and 'logs out'
    """
    session.clear()
    
