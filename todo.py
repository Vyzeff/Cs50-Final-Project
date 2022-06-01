from flask import Blueprint, request, render_template, redirect, make_response, jsonify, session
from models import models, ChangeTodo, CreateTodo, GetTodo


from datetime import datetime
from helpers import error

todo = Blueprint("todo", __name__, static_folder="static", template_folder="templates")


def todoHome(method):
    """
    pagina de checklists.
    é nela onde se deleta e faz o update dos todos ja existentes
    redireciona para outra rota para criar todos
    """
   
    userTodos = GetTodo(session["user_id"])
    
    if method == "GET":
        if GetTodo(session["user_id"], 1) == None:
            return render_template("todo.html", notodo="0")
        return render_template("todo.html", userTodos=userTodos, notodo="1")
    
    if method == "POST":
        return redirect("/todos")
    
    if method == "PUT":
        updateId = request.get_json()
        
        ChangeTodo(updateId, 0)
        return make_response(jsonify({"message":"to-do completed"}))


    if method == "DELETE":
        deleteId = request.get_json()
        
        ChangeTodo(deleteId["input"], 1)
        
    return error("TODO TODOS")

def todoCreate(method):
    """
    generates todos with fetch from input in javascript
    """
    
    if method == "GET":
        return render_template("todos.html")

    
    if method == "POST":
        formInput = request.get_json()  
         
        if formInput == None or formInput == "400":
            return error("Please input valid text.")
    # create a session with the input values
        nowDate = str(datetime.now())
        
        CreateTodo(session["user_id"], formInput["input"], nowDate)
        
        return make_response(jsonify({"message":"to-do added"}))
    