from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import json

class JsonEncodedDict():
    results = 'SELECT * FROM orders;'
    connectToMySQL('coffee_shop').query_db()

class Order():
    def __init__(self,data):
        self.id = data['id'],
        self.invoice = data['invoice'],
        self.customer_id = data['customer_id'],
        self.order_completed = data['order_completed']
        self.price = data['price'],
        self.orders = data['orders']
        self.created_at = data['created_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders"
        results = connectToMySQL('coffee_shop').query_db(query)

        orders = []

        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def add_order(cls,data):
        query = "INSERT INTO orders (invoice,customer_id,price,orders) VALUES (%(invoice)s,%(customer_id)s,%(price)s,%(orders)s);"
        return connectToMySQL('coffee_shop').query_db(query,data)

    @classmethod
    def show_single_user(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s"
        results = connectToMySQL('coffee_shop').query_db(query,data)
        order = cls(results[0])
        print(order)
        return order