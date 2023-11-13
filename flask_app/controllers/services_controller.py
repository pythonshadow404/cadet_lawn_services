from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.service_model import Service


#Render page to select a service
@app.route('/services/new')
def create_page():
    data = {
        "id":session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template('new_service.html', user=user)

@app.route("/services/<int:id>")
def view_service(id):
    data = {
        "id":session["user_id"]
    }
    user = User.get_by_id(data)
    data = {
        "id":id
    }
    service = Service.get_by_id(data)
    return render_template("view_service.html", service=service, user=user)

@app.route("/delete/service/<int:id>")
def remove_service(id):
    data = {
        "id":id
    }
    Service.delete_one(data)
    return redirect("/dashboard")

@app.route("/services/edit/<int:id>")
def edit_service(id):
    data = {
        "id":session["user_id"]
    }
    user = User.get_by_id(data)
    data = {
        "idservice
    }
    service = Service.get_by_id(data)
    return render_template("edit_service.html", service = service, user = user)

@app.route("/create/service", methods=["POST"])
def create_service():
    is_valid = Service.validate_service(request.form)
    if is_valid:
        Service.save(request.form)
        return redirect("/dashboard")
    return redirect('/services/new')

@app.route("/edit/service", methods=["POST"])
def edit_one_service():
    is_valid = Service.validate_service(request.form)
    if is_valid:
        Service.update_one(request.form)
        return redirect("/dashboard")
    return redirect(f"/services/edit/{request.form['user_id']}")
    