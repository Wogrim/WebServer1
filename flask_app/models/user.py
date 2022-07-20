from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from datetime import date

from flask_app.models import language

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UPPERCASE_REGEX = re.compile(r'[A-Z]')
NUMBER_REGEX = re.compile(r'[0-9]')

class User:
    schema = "login_registration_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.language_id = data['language_id']
        self.birthdate = data['birthdate']
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) == 0:
            return False
        #else
        return cls(results[0])
    
    @classmethod
    def read_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) == 0:
            return False
        #else
        return cls(results[0])
    
    @classmethod
    def is_email_in_db(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        return len(results) > 0
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, birthdate, language_id, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(birthdate)s, %(language_id)s, NOW(), NOW());" 
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def validate(cls,data):
        is_valid = True
        if len(data['first_name']) < 2 or len(data['first_name']) > 20:
            is_valid = False
            flash("first name must be 2-20 characters long",'registration')
        if len(data['last_name']) < 2 or len(data['last_name']) > 20:
            is_valid = False
            flash("last name must be 2-20 characters long",'registration')
        if cls.is_email_in_db(data):
            is_valid = False
            flash("an account with that email already exists",'registration')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("invalid email format",'registration')
        if len(data['email']) > 255:
            is_valid = False
            flash("email may not be longer than 255 characters",'registration')
        if len(data['password']) < 8:
            is_valid = False
            flash("password must be at least 8 characters",'registration')
        if (not UPPERCASE_REGEX.search(data['password'])) or (not NUMBER_REGEX.search(data['password'])):
            is_valid = False
            flash("password must have at least 1 number and 1 uppercase letter",'registration')
        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash("passwords must match",'registration')
        
        #language validation
        l_data = {'id':data['language_id']}
        if not language.Language.is_in_db(l_data):
            is_valid=False
            flash("please select a valid language",'registration')

        #birthdate validation 
        birthdate = date.fromisoformat(data['birthdate'])
        today = date.today()
        today_ten_years_ago = date(today.year-10,today.month,today.day)
        #possible leap year problem: on that day there is no day 10 years ago
        if birthdate > today_ten_years_ago:
            is_valid = False
            flash("you must be at least 10 years old to register for our website",'registration')

        return is_valid