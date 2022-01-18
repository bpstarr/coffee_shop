from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
from flask import flash,session

bcrypt = Bcrypt(app)

class Employee():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM employees;"
        results = connectToMySQL('coffee_shop').query_db(query)

        employees = []

        for employee in results:
            employees.append(cls(employee))
        return employees

    @classmethod
    def add_employee(cls,data):
        query = "INSERT INTO employees (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(hashed_pw)s);"
        return connectToMySQL('coffee_shop').query_db(query,data)

    @classmethod
    def show_single_user(cls,data):
        query = "SELECT * FROM employees WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        user = cls(results[0])
        print(user)
        return user

    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash("first name needs to be at least two characters.", category='error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name needs to be at least two characters.", category='error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid. Please try again.", category='error')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("Password needs a minimum of eight characters, at least one letter, one number and one special character.", category='error')
            is_valid = False
        if not PASSWORD_REGEX.match(data['verify_password']):
            flash("Password needs a minimum of eight characters, at least one letter, one number and one special character.", category='error')
            is_valid = False
        query = "SELECT * FROM employees WHERE email = %(email)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        if len(results) != 0:
            flash("Email already exist.Try logging in.", category='error')
            is_valid = False
        if data['password'] != data['verify_password']:
            flash('Passwords must match. Please try again.', category='error')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM employees WHERE email = %(email)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        if len(results)< 1:
            return False
        return cls(results[0])

    @classmethod
    def edit_user(cls,data):
        query = "UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results
        
    @classmethod
    def destroy_user(cls,data):
        query = "DELETE FROM employees WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        return results
            
    @classmethod
    def user_update_validator(cls,data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash("first name needs to be at least two characters.", category='error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name needs to be at least two characters.", category='error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid. Please try again.", category='error')
            is_valid = False
        query2 = "SELECT * FROM employees WHERE id = %(id)s;"
        results2 = connectToMySQL('coffee_shop').query_db(query2,data)
        user2 = cls(results2[0])
        print(user2)
        if data['email'] != session['employee_email']:
            query = "SELECT * FROM employees WHERE email = %(email)s;"
            results = connectToMySQL('coffee_shop').query_db(query,data)
            if len(results) != 0:
                flash("Email already exist.Try logging in.", category='error')
                is_valid = False
        return is_valid

