from itertools import product
from flask import render_template,request,session,flash,redirect,Blueprint,abort,url_for,json
from flask_app import app
from flask_app.models.customer import Customer
from flask_app.models.employee import Employee
from flask_app.models.size import Size
from flask_app.models.menu import Menu
from flask_bcrypt import Bcrypt
import stripe
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'customer_id' in session:
        data = { "id" : session['customer_id']
        }
        quantity_total = 0
        if 'cart' in session:
            for key,product in session['cart'].items():
                quantity_total += int(product['quantity'])
        return render_template('index.html', customers = Customer.show_single_user(data),quantity_total = quantity_total)
    elif 'employee_id' in session:
        data = {"id" :session['employee_id']}
        return render_template('index.html', employees = Employee.show_single_user(data))
    else: 
        data = {
            'id' : ''
        }
        return render_template('index.html')

@app.route('/registration')
def show_registration_page():
    return render_template('register.html')

# register employee
@app.route('/employee/register', methods = ['POST']) 
def register_employee():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password'],
        'verify_password':request.form['verify_password']
    }
    valid = Employee.user_validator(data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        data['hashed_pw'] = hashed_pw
        employee = Employee.add_employee(data)
        employee_email = Employee.get_by_email(data)
        session['employee_email'] = employee_email.email
        session['employee_id'] = employee
        print('User logged in.')
        flash('Login Successful.' , category='success')
        return redirect ('/menu')
    return redirect('/registration')

# register customer
@app.route('/customer/register', methods = ['POST']) 
def register_customer():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password'],
        'verify_password':request.form['verify_password']
    }
    valid = Customer.user_validator(data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        data['hashed_pw'] = hashed_pw
        customer = Customer.add_customer(data)
        customer_email = Customer.get_by_email(data)
        session['customer_email'] = customer_email.email
        session['customer_id'] = customer
        print('User logged in.')
        flash('Login Successful.', category='success')
        return redirect ('/menu')
    return redirect('/registration')

@app.route('/login')
def show_login_page():
    return render_template('login.html')

# Login customer
@app.route('/customer/login',methods = ['POST'])
def login_customer():
    customer = Customer.get_by_email(request.form)
    if not customer:
        flash("Invalid email or Password. Please try again.",category='error')
        return redirect('/login')
    if not bcrypt.check_password_hash(customer.password,request.form['password']):
        flash('invalid email or password. Please try again.', category='error')
        return redirect('/login')
    session['customer_id'] = customer.id
    session['customer_email'] = customer.email
    print('successful login')
    flash('Login Successful',category = 'success')
    return redirect ('/menu')

# Login employee
@app.route('/employee/login',methods = ['POST'])
def login_employees():
    employee = Employee.get_by_email(request.form)
    if not employee:
        flash("Invalid email or Password. Please try again.",category='error')
        return redirect('/login')
    if not bcrypt.check_password_hash(employee.password,request.form['password']):
        flash('invalid email or password. Please try again.', category='error')
        return redirect('/login')
    session['employee_id'] = employee.id
    session['employee_email'] = employee.email
    print('successful login')
    flash('Login successful', category='success')
    return redirect ('/menu')

@app.route('/menu')
def show_menu():
    image_file = url_for('static', filename = 'pics/')
    if 'customer_id' in session:
        user_data = {
            'id' : session['customer_id']
        } 
        quantity_total = 0
        if 'cart' in session:
            for key,product in session['cart'].items():
                quantity_total += int(product['quantity'])
        return render_template('menu.html',customers = Customer.show_single_user(user_data),show_items = Menu.get_all(),image_file = image_file,quantity_total = quantity_total)
    elif 'employee_id' in  session:
        user_data = {
            'id' : session['employee_id']
        }
        return render_template('menu.html', employees = Employee.show_single_user(user_data),show_items = Menu.get_all(),image_file = image_file)
    else: 
        quantity_total = 0
        return render_template('menu.html',show_items = Menu.get_all(),image_file = image_file,quantity_total = quantity_total)

@app.route('/logout')
def logout():
    session.clear()
    flash('logout successful', category = "success")
    print('logout successful')
    return redirect('/')

@app.route('/customer/<int:id>')
def show_customer_page(id):
    if 'customer_id' not in session:
        return redirect('logout')
    data = {
        'id':session['customer_id']
    }
    quantity_total = 0
    if 'cart' in session:
        for key,product in session['cart'].items():
            quantity_total += int(product['quantity'])
            return render_template('edit_customer.html',customer = Customer.show_single_user(data),quantity_total = quantity_total)
    return render_template('edit_customer.html',customer = Customer.show_single_user(data),quantity_total = quantity_total)

@app.route('/edit_customer/<int:id>',methods = ['GET','POST'])
def edit_account_customer(id):
    if 'customer_id' not in session:
        return redirect('/')
    data = {
        'id':id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
    valid = Customer.user_update_validator(data)
    if not valid:
        return redirect(f'/user/{id}')
    print(valid)
    if valid:
        user = Customer.edit_user(data)
        print(user)
        flash('Updates successful.', category='success')
        return redirect('/menu')

@app.route('/employee/<int:id>')
def show_employee_edit_page(id):
    if "employee_id" not in session:
        return redirect('/logout')
    data = {
        "id":session["employee_id"]
    }
    return render_template('edit_employee.html',employee = Employee.show_single_user(data))

@app.route('/edit_employee/<int:id>',methods = ['GET','POST'])
def edit_account_employee(id):
    if 'employee_id' not in session:
        return redirect('/')
    data = {
        'id':id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
    valid = Employee.user_update_validator(data)
    if not valid:
        return redirect(f'/employee/{id}')
    print(valid)
    if valid:
        user = Employee.edit_user(data)
        print(user)
        flash('Updates successful.', category='success')
        return redirect('/menu')

@app.route('/destroy_customer/<int:id>')
def destroy_customer(id):
    if 'customer_id' not in session:
        return redirect('/')
    data = {
        'id':session['customer_id']
    }
    Customer.destroy_user(data)
    flash('Account Deleted')
    return redirect('/')

@app.route('/destroy_employee/<int:id>')
def destroy_employee(id):
    if 'employee_id' not in session:
        return redirect('/')
    data = {
        'id':session['customer_id']
    }
    Employee.destroy_user(data)
    flash('Account Deleted')
    return redirect('/')





    
    
    


        

