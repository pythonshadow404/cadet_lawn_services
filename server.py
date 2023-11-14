#Cadel Lawn/server.py
from flask_app import app
from flask_app.controllers import users_controller, services_controller, home_controller

if __name__ == "__main__":
    app.run(debug=True)