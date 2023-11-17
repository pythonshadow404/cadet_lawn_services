from lawn_app import app
from flask import request, render_template, redirect, session, url_for
from lawn_app.models.loregs import User
from lawn_app.models.service_model import Request
from datetime import date, datetime, timedelta


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id']
    }
    user = User.get_one(data)
    services = Request.get_all(data)
    return render_template('user_page.html', user = user, uservice = services)

@app.route('/create_service')
def addservice():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    today = date.today()
    tomorrow = today + timedelta(1)
    return render_template('add.html', user = user, tomorrow = tomorrow)

@app.route('/addservice', methods=['POST'])
def saveservice():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'mowing' : request.form['mowing'],
        'aeration': request.form['aeration'],
        'prunning': request.form['prunning'],
        'fertilize': request.form['fertilize'],
        'date': "",
        'notes' : request.form['notes'],
        'user_id' : session['user_id'],
        'reldate': request.form['date']
    }
    valid = Request.validation_service(data)
    if valid: 
        start = datetime.strptime(data['reldate'], '%Y-%m-%d')
        data['date'] = datetime.strftime(start, "%b %d %Y")
        Request.save(data)
        return redirect('/dashboard')
    return redirect('/create_service')

@app.route('/services/update/<int:service_id>')
def update(service_id):
    if 'user_id' not in session:
        return redirect('/') 
    session['service_id'] = service_id
    service = Request.get_one(service_id)
    data = {
        'user_id': session['user_id'],
    }
    user = User.get_one(data)
    sdate = service.date
    return render_template('edit.html', service = service, user = user, sdate = sdate)

@app.route('/services/edit', methods=['POST'])
def editservice():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'mowing' : request.form['mowing'],
        'aeration': request.form['aeration'],
        'prunning': request.form['prunning'],
        'fertilize': request.form['fertilize'],
        'date': "",
        'notes' : request.form['notes'],
        'user_id' : session['user_id'],
        'reldate': request.form['date']
    }
    valid = Request.validation_service(data)
    if valid: 
        start = datetime.strptime(data['reldate'], '%Y-%m-%d')
        data['date'] = datetime.strftime(start, "%b %d %Y")
        Request.save(data)
        return redirect('/dashboard')
    return redirect(url_for('update', service_id = session['service_id']))

@app.route("/services/delete/<int:service_id>")
def remove_service(service_id):
    data = {
        "service_id": service_id
    }
    Request.delete_one(data)
    return redirect("/dashboard")


@app.route('/services/<int:service_id>')
def display(service_id):
    if 'user_id' not in session:
        return redirect('/')
    service = Request.get_one(service_id)
    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    return render_template('showpage.html', service = service, user = user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')