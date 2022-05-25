from flask import Flask, render_template, redirect, session, request
from flask_session import Session

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy_utils import database_exists, create_database

from datetime import datetime
from helper import login_verify, error

# Configures the app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Makes so data is saved in files
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Defines flask session
Session(app)

#Defines metadata from sqlalchemy
metaObj = MetaData()
# Creates engine for SQLAlchemy
engine = create_engine("sqlite+pysqlite:///homebook.db", echo=True, future=True)
# If Database isn't present, create one
if not database_exists(engine.url):
    create_database(engine.url)
    
#    user_table = Table(
#    "user_account",
#    metaObj,
#   Column('id', Integer, primary_key=True),
#    Column('name', String(30)),
#    Column('fullname', String) )
 
@app.route("/")
@login_verify
def index():
    #TODO
    # Pagina base com a sidebar, temperatura e dia.
    # Um relogio
    # themes: dark, light, gray, purple, orange and let the user customize the colors and font for themselves
    # notas mais recentes
    # uma checklist vai aparecer, a que tem a flag de "importante"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # will ask for an unused username
    # will ask for a password ate least 8 digits long, together with 1 number and 1 symbol
    # maybe implement captcha???
    # must have invalid when input user already exists in db
    if request.method == "GET":
        return render_template("register.html")
    
    
    if not request.form.get("username"):
        return render_template("register.html", invalid="1")
    
    if not request.form.get("password"):
        return render_template("register.html", invalid="2")
    
    if request.form.get("password") != request.form.get("confirm"):
        return render_template("register.html", invalid=3)
    with engine.connect() as conn:
        
    userLow = 
    return error("TODO")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    # will redirect to login page
    # will take a username and password
    # check if those things are in db
    # either log in or error popup
    # Forgets user
    # when user and/or password go wrong, reload with invalid for html if
    return error("TODO")
    session.clear()
    
    #if request.method == "GET":
    #    return render_template("login.html")
    
    
    #session["user_id"] = rows[0]["id"]

@app.route("/logout")
def logout():
    
    session.clear()
    
    return redirect("/")

@app.route("/notebook")
def notebook():
    # will let the user take notes in separate blocks which can be arranged
    # will show all notes
    # notas vao ter titulo, data e corpo
    return error("TODO")

@app.route("/clock")
def clocks():
    # timers e relogios
    # eh possivel escolher relogios de outras regioes
    # criar alarmes e timers
    # multiplos relogios ao mesmo tempo
    return error("TODO")

@app.route("/checklist")
def checklists():
    # pagina de checklists.
    # vai ser possivel criar uma ou mais checklists
    # uma delas pode ser dada como "importante" e vai aparecer na index
    # da mesma forma do notebook, elas podem ser arrastadas por ai
    return error("TODO")

@app.route("/water")
def waterBottle():
    # contador de agua
    # meta diaria
    # botao para tomar agua
    # cicla entre imagens de uma garrafa de agua
    # form com botao para tomar uma medida de agua definida pelo usuario
    return error("TODO")