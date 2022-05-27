function firstCreate() {
    //remove div that is telling user to create
    var remove = document.getElementById("removable");
    remove.remove();

    //create new button for creating other lists
    var newCreate = document.createElement("button");
    var newText = document.createTextNode("Create New To-Do List");
    newCreate.appendChild(newText);
    newCreate.classList.add("btn", "btn-secondary", "btn-switch", "mx-auto", "w-auto");
    newCreate.setAttribute("type", "submit");
    newCreate.setAttribute("onclick", "todoCreate()");


    //insert button on main
    var exists = document.getElementById("first");
    exists.appendChild(newCreate);
    todoCreate();
}

function todoCreate() {
    //create new button for creating other lists
    var todoForm = document.createElement("form");
    todoForm.setAttribute("method", "post");
    todoForm.setAttribute("action", "/todo");
    todoForm.classList.add( "mx-auto", "w-auto");


    var todoTitle = document.createElement("input");
    todoTitle.classList.add( "mx-auto", "w-auto");
    todoTitle.id = "todoTitle"
    todoTitle.setAttribute("placeholder", "Title");
    todoTitle.setAttribute("type", "text");
    todoForm.appendChild(todoTitle);
    todoForm.appendChild(document.createElement("br"));

    var todoCheck = document.createElement("button");
    todoCheck.setAttribute("type", "checkbox");
    todoCheck.setAttribute("onclick","strikeText"); //()
    todoCheck.classList.add("form-check-input");
    todoForm.appendChild(todoCheck);

    var todoText = document.createElement("input");
    todoText.setAttribute("type", "text");
    todoText.setAttribute("placeholder", "To-Do");
    todoText.classList.add( "mx-auto", "w-auto");
    todoForm.appendChild(todoText);
    todoForm.appendChild(document.createElement("br"));





    //insert button on main
    var append = document.getElementById("anchor");
    append.appendChild(todoForm);
}

function strikeText(){
    //na checkbox dele, vai fazer o input daquela checkbox ficar riscado <s>
}