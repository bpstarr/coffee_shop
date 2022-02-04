from flask_app.models.menu import Menu
from flask_app.models.customer import Customer
from flask_app.models.employee import Employee
from flask_app.models.size import Size
from flask_app import app
from flask import redirect,request, session,url_for,flash,render_template

@app.route('/cart')
def show_user_cart():
    if 'customer_id' not in session:
        flash('need to login or register')
        return redirect('/menu')
    elif 'cart' not in session or len(session['cart']) <=0:
        flash('Cart is empty.')
        return redirect('/menu')
    else: 
        user_data = {
            'id' : session['customer_id']
        }
    sub_total = 0
    grand_total = 0
    quantity_total = 0
    for key,product in session['cart'].items():
        sub_total += float(product['price'])* int(product['quantity'])
        grand_total = float("%.2f" % sub_total)
        quantity_total += float("%d" % int(product['quantity']))
        print(quantity_total)
    
    return render_template('cart.html', customers = Customer.show_single_user(user_data),grand_total = grand_total, quantity_total = quantity_total)

def allDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+ list(dict2.items()))
    return False

@app.route('/add_to_cart', methods = ['POST'])
def add_product_to_cart():
    if "customer_id" not in session:
        flash('please login to use cart')
        return redirect('/menu')
    try:
        product_id = request.form.get('product_id')
        size_name = request.form.get('size_name')
        if size_name == '':
            flash('Size needs to be selected.')
            return redirect('/menu')
        quantity = int(request.form.get('quantity'))
        user_data = {
            "product_id":product_id
        }
        size_data = {
            'size_name': size_name,
            'product_id':product_id
        }
        product = Menu.show_single_item(user_data)
        size = Size.show_single_size_and_product(size_data)
        if request.method == "POST": 
            size_id = str(size.id)
            print(size.id)
            DictItems = {size_id:{'name':product.name, 'price':float(size.price),'size':size.name, 'quantity':quantity}}
            if 'cart' in session:
                print(session['cart'])
                if size_id in session['cart']:
                    for key, item in session['cart']:
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                            flash('quantity Updated',category = 'success')
                else: 
                    session['cart'] = allDicts(session['cart'],DictItems)
                    flash('Item Added to cart',category = 'success')
                    return redirect('/menu')
            else:
                session['cart'] = DictItems
                flash('Item Added to Cart',category = 'success')
                print(session['cart'])
                return redirect('/menu')
    except Exception as e:
        print(e)
        flash('Item already in cart. Update quantity in cart.')
        return redirect('/menu')
    finally: redirect('/menu')

@app.route('/update_cart/<int:code>', methods = ['POST'])
def update_cart(code):
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect('/menu')
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    print(session['cart'])
                    flash('item is updated', category = 'success')
                    return redirect(url_for('show_user_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('show_user_cart'))

@app.route('/deleteitem/<int:id>')
def delete_item(id):
    if 'cart' not in session or len(session['cart']) <=0:
        session.pop('cart',None)
        return('/menu')
    try: 
        session.modified = True
        for key, item in session['cart'].items():
            if int(key) == id:            
                session['cart'].pop(key,None)
                flash('item deleted')
                return redirect(url_for('show_user_cart'))

    except Exception as e:
        print(e)
        return redirect('/cart')

@app.route('/clearcart')
def clear_cart():
    try: 
        session.pop('cart',None)
        return redirect('menu')
    except Exception as e:
        print(e)