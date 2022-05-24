from flask import Flask, render_template, redirect, session, request
from flask_session import Session
from helper import login_verify, error

app = Flask(__name__)
Session(app)

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
@app.route("/login", methods=["GET", "POST"])
def login():
    # will redirect to login page
    # will take a username and password
    # check if those things are in db
    # either log in or error popup
    db.execute bla bla bla
    session.clear()
    session["user_id"] = rows[0]["id"]

@app.route("/register",)
def register():
    # will ask for an unused username
    # will ask for a password ate least 8 digits long, together with 1 number and 1 symbol
    # maybe implement captcha???

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/notebook")
def notebook():
    # will let the user take notes in separate blocks which can be arranged
    # will show all notes
    # notas vao ter titulo, data e corpo

@app.route("/clock")
def clocks():
    # timers e relogios
    # eh possivel escolher relogios de outras regioes
    # criar alarmes e timers
    # multiplos relogios ao mesmo tempo

@app.route("/checklist")
def checklists():
    # pagina de checklists.
    # vai ser possivel criar uma ou mais checklists
    # uma delas pode ser dada como "importante" e vai aparecer na index
    # da mesma forma do notebook, elas podem ser arrastadas por ai

@app.route("/water")
def waterBottle():
    # contador de agua
    # meta diaria
    # botao para tomar agua
    # cicla entre imagens de uma garrafa de agua
    # form com botao para tomar uma medida de agua definida pelo usuario