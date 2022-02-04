import secrets
import stripe
import os
import ast
import smtplib
import pdfkit
import json
from flask_mail import Message, Mail
from flask import render_template,request,session,flash,redirect,url_for,make_response,jsonify
from flask_app import app
from flask_app.models.customer import Customer
from flask_app.models.employee import Employee
from flask_app.models.order import Order

@app.route('/get_order')
def get_order():
    if 'customer_id' not in session:
        return ('/logout')
    data = {
        'customer_id' : session['customer_id'],
        'invoice' : secrets.token_hex(5),
        'orders' : str(session['cart'])
    }
    try:
        Order.add_order(data)             
        flash('Your order has been sent successfully',category = 'success')
        session.pop('cart')
        invoice = data['invoice']
        return redirect(f'/orders/{invoice}')
    except Exception as e:
        print(e)
        flash('Something went wrong with getting order')
        return redirect('/cart')

@app.route('/orders/<invoice>')
def orders(invoice):
    if 'customer_id' not in session:
        return ('/logout')
    grand_total = 0
    sub_total = 0
    user_data  = {
        'id':session['customer_id']
    }
    order_data = {
        'invoice':invoice
    }
    customer = Customer.show_single_user(user_data)
    order = Order.show_single_order_by_invoice(order_data)
    tuple_order = ast.literal_eval(order.orders)
    print(tuple_order)
    for _key, product in tuple_order.items():
        sub_total += float(product['price']*int(product['quantity']))
        grand_total = ("%.2f" % float(sub_total))
    print(grand_total)
    return render_template('customer_order.html',tuple_order = tuple_order, sub_total = sub_total, grand_total = grand_total, customers = customer,order = order, invoice = invoice )

@app.route('/get_pdf/<invoice>', methods = ['POST'])
def get_pdf(invoice):
    if 'customer_id' not in session:
        return redirect('/logout')
    grand_total = 0
    sub_total = 0
    if request.method == 'POST':
        user_data  = {
        'id':session['customer_id']
        }
        order_data = {
            'invoice':invoice
        }
        customer = Customer.show_single_user(user_data)
        order = Order.show_single_order_by_invoice(order_data)
        tuple_order = ast.literal_eval(order.orders)
        for _key, product in tuple_order.items():
            sub_total += float(product['price'])* int(product['quantity'])
            grand_total = float("%.2f" % sub_total)
        rendered = render_template('customer_pdf.html',invoice = invoice, grand_total = grand_total, customers = customer, order = order,tuple_order = tuple_order)
        pdf = pdfkit.from_string(rendered,False)
        response = make_response(pdf)
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'inline: filename='+invoice+'.pdf'
        return response
    return request(url_for('orders'))

publishable_key = 'pk_test_51KGDLWG4Gp97ezol1gzdxfeNffhhdRC8nr4oqm2b7Mrh5mukNlMIiih7hL3q3XsVqx1oDpwMAcxH7yHRJOT0sIjt007U3MqFfP'
stripe.api_key = os.environ.get("stripe.api_key")

@app.route('/payment', methods = ['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email = request.form['stripeEmail'],
        source = request.form['stripeToken']
    )
    charge = stripe.Charge.create(
        customer = customer.id,
        description = 'Myshop',
        amount = amount,
        currency = 'usd',
    )
    order_data = {
        'invoice': request.form.get('invoice'),
        'paid': 'yes'
    }
    Order.edit_payment_status(order_data)
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    data = {
        'id':session['customer_id']
    }
    customers = Customer.show_single_user(data)
    return render_template('thanks.html', customers = customers)

@app.route('/order_board') 
def show_order_board():
    if 'employee_id' not in session:
        return redirect('/logout')
    user_data = {
        'id' : session['employee_id']
    }
    all_orders = Order.get_all_with_customer_info()
    employees = Employee.show_single_user(user_data)
    return render_template('order_board.html',employees = employees, all_orders = all_orders)

@app.route('/order_fulfilled', methods = ['GET','POST'])
def order_fulfilled():
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        'invoice' : request.form.get('invoice'),
        'customer_email': request.form.get('customer_email')
    }
    unpacked_invoice  = {"invoice": eval(data['invoice'].replace('(',"").replace((")"),"").replace(",",""))}
    if request.method == 'POST':
        Order.update_order_status(unpacked_invoice)
        flash('Order Updated', category= 'success')
        print(data['customer_email'])
    

    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '1dd10e9522fd3b'
    app.config['MAIL_PASSWORD'] = 'f98dcd8e4d6dad'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail = Mail(app)
    message = Message("Your Order is Ready",sender = f"{session['employee_email']}",recipients = [f"{data['customer_email']}"])
    message.body = f"Your Order is Ready. Your order is ready for pickup.Here is the invoice number:{unpacked_invoice['invoice']}"
    mail.send(message)
    return redirect('/order_board')
