from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.customer import Customer
import ast

class Order():
    def __init__(self,data):
        self.id = data['id'],
        self.invoice = data['invoice'],
        self.customer_id = data['customer_id'],
        self.order_status = data['order_status']
        self.orders = data['orders']
        self.created_at = data['created_at']
        self.paid = data['paid']
        self.order_fulfilled = data['order_fulfilled']
        self.tuple_order = eval(data['orders'])
        self.creator = None

        def __repr__(self):
            return '<Order %r>' % self.invoice

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('coffee_shop').query_db(query)

        orders = []

        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def get_all_with_customer_info(cls):
        query = "SELECT * FROM orders LEFT JOIN customers ON orders.customer_id = customers.id;"
        results = connectToMySQL('coffee_shop').query_db(query)
        list = []

        for object in results:
            customer_data = {
                "id":object['customers.id'],
                "first_name":object['first_name'],
                "last_name":object['last_name'],
                "email":object['email'],
                "password":object['password'],
                "created_at":object['customers.created_at'],
                "updated_at":object['updated_at'],
                "customer_id":object['customer_id']
            }
            t = cls(object)
            t.creator = Customer(customer_data)
            list.append(t)
        return list


    @classmethod
    def add_order(cls,data):
        query = "INSERT INTO orders (invoice,customer_id,orders) VALUES (%(invoice)s,%(customer_id)s,%(orders)s);"
        return connectToMySQL('coffee_shop').query_db(query,data)

    @classmethod
    def show_single_order(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        order = cls(results[0])
        print(order)
        return order

    @classmethod
    def show_single_order_by_invoice(cls,data):
        query = "SELECT * FROM orders WHERE invoice = %(invoice)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        order = cls(results[0])
        print(order)
        return order
    
    @classmethod
    def edit_payment_status(cls,data):
        query = "UPDATE orders SET paid = %(paid)s WHERE invoice = %(invoice)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod
    def update_order_status(cls,data):
        query = "UPDATE orders SET order_fulfilled = 'yes' WHERE invoice = %(invoice)s"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        print(results)
        return results

    @classmethod
    def show_single_order_with_customer(cls,data):
        query = "SELECT * FROM orders LEFT JOIN customers ON orders.customer_id = customers.id WHERE invoice = %(invoice)s;"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        list = []

        for object in results:
            customer_data = {
                "id":object['customers.id'],
                "first_name":object['first_name'],
                "last_name":object['last_name'],
                "email":object['email'],
                "password":object['password'],
                "created_at":object['customers.created_at'],
                "updated_at":object['updated_at'],
                "customer_id":object['customer_id']
            }
            t = cls(object)
            t.creator = Customer(customer_data)
            list.append(t)
        return list[0]