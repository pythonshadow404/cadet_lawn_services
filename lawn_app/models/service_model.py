import re
from flask import flash
from lawn_app.config.mysqlconnection import connectToMySQL

class Request:

    def __init__(self, data):
        self.service_id = data['service_id']
        self.mowing = data['mowing']
        self.aeration = data['aeration']
        self.prunning = data['prunning']
        self.fertilize = data['fertilize']
        self.date = data['date']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.reldate = data['reldate']

    def __repr__(self):
        return self.service_id
    
    @staticmethod
    def validation_service(data):
        is_valid = True
        if len(data['reldate']) < 8:
            flash('Date must be in xx/xx/xxx format', 'rsvp')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO services (mowing, aeration, prunning, fertilize, date, notes, user_id, reldate)
                    VALUES (%(mowing)s, %(aeration)s, %(prunning)s, %(fertilize)s, %(date)s, %(notes)s, %(user_id)s, %(reldate)s)"""
        results = connectToMySQL('lawn_schema').query_db(query, data)
        return results 
    
    @classmethod 
    def update(cls, data):
        query = """INSERT INTO services (mowing, aeration, prunning, fertilize, date, notes, reldate)
                    VALUES (%(mowing)s, %(aeration)s, %(prunning)s, %(fertilize)s, %(date)s, %(notes)s, %(reldate)s)"""
        results = connectToMySQL('lawn_schema').query_db(query, data)
        return results
    
    @classmethod
    def get_one(cls, service_id): 
        query = """SELECT * FROM services WHERE service_id = %(service_id)s"""
        data = {
            'service_id': service_id
        }
        results = connectToMySQL('lawn_schema').query_db(query, data)
        service = cls(results[0])
        return service
    
    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM services WHERE user_id = %(user_id)s"""
        results = connectToMySQL('lawn_schema').query_db(query, data)
        services = []
        for service in results:
            services.append(cls(service))
        return services
    
    @classmethod
    def delete_one(cls, data):
        query = """DELETE FROM services WHERE service_id = %(service_id)s"""
        results = connectToMySQL('lawn_schema').query_db(query, data)
        return results 