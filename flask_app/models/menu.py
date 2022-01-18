from flask_app import app
from logging import NullHandler
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session
import os
from flask_app.models.size import Size


class Menu():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.picture = data['picture']
        self.category = data['category']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM menu"
        results = connectToMySQL('coffee_shop').query_db(query)

        items = []

        for item in results:
            items.append(cls(item))
        return items

    @classmethod
    def get_all_with_sizes(cls):
        query = "SELECT * FROM menu LEFT JOIN sizes ON menu.id = sizes.menu_id;"
        results = connectToMySQL('songs').query_db(query)
        list = []

        for object in results:
            menu_data = {
                'name':object['name'],
                'description':object['description'],
                'created_at':object['created_at'],
                'updated_at':object['updated_at'],
                'picture':object['picture'],
                'category':object['category'],                    
                'id':object['sizes.id'],
                'size_name':object['sizes.name'],
                'price':object['sizes.price'],
                'menu_id':object['sizes.menu_id']
            }
            t = cls(object)
            t.creator = Menu(menu_data)
            list.append(t)
        return list

    @classmethod
    def get_all_with_sizes_from_id(cls,data):
        query = "SELECT * FROM menu LEFT JOIN sizes ON menu.id = sizes.menu_id WHERE menu.id = %(product_id)s AND sizes.name = %(size_name)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        list = []

        for object in results:
            menu_data = {
                'name':object['name'],
                'description':object['description'],
                'created_at':object['created_at'],
                'updated_at':object['updated_at'],
                'picture':object['picture'],
                'category':object['category'],                    
                'size_id':object['sizes.id'],
                'size_name':object['sizes.name'],
                'price':object['sizes.price'],
                'menu_id':object['sizes.menu_id']
            }
            t = cls(object)
            t.creator = Menu(menu_data)
            list.append(t)
        return list[0]

    @classmethod 
    def add_menu(cls,data):
        query = "INSERT INTO menu (name,description,picture,category) VALUES (%(name)s,%(description)s,%(picture)s,%(category)s);"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod
    def edit_menu(cls,data):
        query = "UPDATE menu SET name = %(name)s,description = %(description)s,category = %(category)s WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod
    def show_single_item(cls,data):
        query = "SELECT * FROM menu WHERE id = %(product_id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        item = cls(results[0])
        return item

    @classmethod
    def edit_image(cls,data):
        query = "UPDATE menu SET picture = %(picture)s WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod 
    def menu_validator(cls,data):
        is_valid = True
        if len(data['name']) < 2:
            flash('name must be longer than two characters')
            is_valid = False
        if len(data['description']) < 2:
            flash('description must be more than two characters')
            is_valid = False 
        query = "SELECT * FROM menu WHERE name = %(name)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        if len(results) != 0:
            flash("Name already exists. Please pick a different name")
            is_valid = False
        EXT = {'.jpeg','.jpg','.png'}
        root_ext = os.path.splitext(data['picture'])
        if root_ext[1] not in EXT:
            flash('File type must be jpg,jpeg or png.')
            is_valid = False
        if len(data['category']) < 2:
            flash('category must be more than two characters')
            is_valid = False
        return is_valid
    
    @classmethod
    def show_customers_cart(cls,data):
        query = "SELECT * FROM menu WHERE id = %(id)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)

        items = []

        for item in results:
            items.append(cls(item))
        print(items)
        return items

    @classmethod 
    def edit_menu_validator(cls,data):
        is_valid = True
        if len(data['name']) < 2:
            flash('name must be longer than two characters')
            is_valid = False
        if len(data['description']) < 2:
            flash('description must be more than two characters')
            is_valid = False 
        if len(data['category']) < 2:
            flash('category must be more than two characters')
            is_valid = False
        return is_valid

    @classmethod 
    def edit_menu_validator_pic(cls,data):
        is_valid = True
        EXT = {'.jpeg','.jpg','.png'}
        root_ext = os.path.splitext(data['picture'])
        if root_ext[1] not in EXT:
            flash('File type must be jpg,jpeg or png.')
            is_valid = False
        return is_valid



    
        