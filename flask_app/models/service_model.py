from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Service:
    DB = 'lawn_schema'
    def __init__(self, data):
        self.request_id = data['service_id']
        self.service = data['service']
        self.date = data['date']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def __repr__(self):
        return self.service
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO request (service, date, notes, user_id)
                    VALUES (%(service)s, %(date)s, %(notes)s, %(user_id)s)"""
        results = connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM services;"
        results = connectToMySQL(cls.DB).query_db(query)
        services = []
        for service in results:
            services.append(cls(service))
        return services

    @classmethod
    def get_by_id(cls, data): 
        query = """SELECT * FROM services WHERE service_id = %(service_id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod 
    def update(cls, data):
        query = """UPDATE services SET service = %(service)s, date = %(date)s, notes = %(notes)s,
                    WHERE service_id = %(service_id)s """
        return connectToMySQL('DB').query_db(query, data)
    
    @classmethod
    def delete_one(cls, data):
        query = """DELETE FROM services WHERE service_id = %(service_id)s"""
        return connectToMySQL('DB').query_db(query, data)
    
    @staticmethod
    def validation_service(service_dict):
        is_valid = True

        if len (service_dict['service']) == 0:
            flash('Please choose a service!')
            is_valid = False
        if len(service_dict['date']) == 0:
            flash('Date must be in xx/xx/xxx format', 'rsvp')
            is_valid = False
        return is_valid