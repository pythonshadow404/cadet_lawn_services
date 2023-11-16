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
        "service_id":id
    }
    service = Service.get_by_id(data)
    print(service)
    return render_template("view_service.html", service=service, user=user)

@app.route("/delete/service/<int:id>")
def remove_service(id):
    data = {
        "service_id":id
    }
    Service.delete_one(data)
    print("=================",data)
    return redirect("/dashboard")

@app.route("/services/edit/<int:service_id>")
def edit_service(id):
    data = {
        "id":session["user_id"]
    }
    user = User.get_by_id(data)
    data = {
        "service_id":id
    }
    service = Service.get_by_id(data)
    print("#############We are in the edit route##################")
    return render_template("edit_service.html", service = service, user = user)

@app.route("/create/service", methods=["POST"])
def create_service():
    is_valid = Service.validate_service(request.form)
    print(request.form)
    data = {
        'mowing':None,
        'aeration':None,
        'prunning':None,
        'fertilizer':None,
        'date':request.form['date'],
        'notes':request.form['notes'],
        'user_id':request.form['user_id'],
    }
    if request.form.get('mowing'):
        data['mowing'] = request.form['mowing']
    if request.form.get('fertilizer'):
        data['fertilizer'] = request.form['fertilizer']
    if request.form.get('prunning'):
        data['prunning'] = request.form['prunning']
    if request.form.get('aeration'):
        data['aeration'] = request.form['aeration']

    if is_valid:
        Service.save(data)
        return redirect("/dashboard")
    return redirect('/services/new')

@app.route("/edit/service", methods=["POST"])
def edit_one_service():
    is_valid = Service.validate_service(request.form)
    if is_valid:
        Service.update_one(request.form)
        return redirect("/dashboard")
    return redirect(f"/services/edit/{request.form['user_id']}")
    