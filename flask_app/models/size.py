from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Size():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.menu_id = data['menu_id']
        
    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM sizes;"
        results = connectToMySQL('coffee_shop').query_db(query,data)

        sizes = []

        for size in results:
            sizes.append(cls(size))
        return sizes

    @classmethod
    def show_single_size_and_product(cls,data):
        query = "SELECT * FROM sizes WHERE name = %(size_name)s AND menu_id = %(product_id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        size = cls(results[0])
        return size

    @classmethod
    def show_product_and_sizes(cls,data):
        query = "SELECT * FROM sizes WHERE menu_id = %(menu_id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        product = cls(results[0])
        return product
    
    @classmethod
    def add_size(cls,data):
        query = "INSERT INTO sizes (name,price,menu_id) VALUES (%(name)s,%(price)s,%(menu_id)s);"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod
    def edit_size(cls,data):
        query = "UPDATE sizes SET price = %(price)s WHERE menu_id = %(product_id)s AND name = %(name)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def size_validator(cls,data):
        PRICE_REGEX = re.compile(r'\d{0,2}(\.\d{1,2})?')
        is_valid = True
        if len(data['name']) <=0:
            flash('Size name must be selected.')
            is_valid = False
        if len(data['price']) < 2:
            flash('Price must be greater than 2 characters')
            is_valid = False
        try:
            if int(data['price']) < 0:
                flash('Price must be positive')
                is_valid = False
        except ValueError:
            print('it is False')
        if not PRICE_REGEX.match(data['price']):
            flash('Price must be a number')
            is_valid = False
        query = "SELECT * FROM sizes WHERE menu_id = %(menu_id)s && name = %(name)s"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        if len(results) > 0:
            flash("Item already has price. Please go to edit.")
            is_valid = False
        return is_valid

    @classmethod
    def size_update_validator(cls,data):
        PRICE_REGEX = re.compile(r'\d{0,2}(\.\d{1,2})?')
        is_valid = True
        if len(data['name']) <= 0:
            flash('Size name must be selected.')
            is_valid = False
        if len(data['price']) <= 2:
            flash('Price must be greater than 2 characters')
            is_valid = False
        try:
            if int(data['price']) < 0:
                flash('Price must be positive')
                is_valid = False
        except ValueError:
            print('it is False')
        if not PRICE_REGEX.match(data['price']):
            flash('Price must be a number')
            is_valid = False

        return is_valid
        




