from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import menus
from flask_app.controllers import carts
from flask_app.controllers import orders
import os

app.secret_key = os.environ.get("SECRET_KEY")

if __name__ == "__main__":
    app.run(debug= True)