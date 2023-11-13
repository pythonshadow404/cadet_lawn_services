from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.service_model import Service
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "lawn_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.services = []

    @classmethod
    def save(cls, data):
        # INSERT always return an ID back
        query = "INSERT INTO users (first_name, last_name, email, password)\
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        #email is the only thing we need
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1: #login verification: if no email came back then the email does not exist.
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN services ON users.id= services.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        user = cls(results[0])
        for row in results:
            service_data = {
                "id":row["service_id"],
                "service":row["service"],
                "date":row["date"],
                "notes":row["notes"],
                "created_at":row["services.created_at"],
                "updated_at":row["services.updated_at"],
                "user_id":row["id"],
                }
            user.services.append(Service(service_data))
        return user
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.DB).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password name must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid
    
        