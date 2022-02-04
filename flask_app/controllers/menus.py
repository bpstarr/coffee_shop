from werkzeug.utils import secure_filename
from flask_app import app
from flask import redirect,request, session,url_for,flash,render_template,json,jsonify,Flask,Response
from flask_app.models.menu import Menu
from flask_app.models.employee import Employee
from flask_app.models.size import Size
import os,json
from flask_app import ALLOWED_EXTENSIONS

def allowed_file(pics):
    return '.' in pics and \
        pics.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create_item', methods = ['POST'])
def create_item():
    if 'employee_id' not in session:
        return redirect('/logout')
    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file Part')
            return redirect('/menu')
        file = request.files['picture']
        if file.filename =='':
            flash ('Please select file')
            return redirect('/menu')
        if file and allowed_file(file.filename):
            pics = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pics))
        
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'picture' : request.files['picture'].filename,
        'category':request.form['category']
    }
    valid = Menu.menu_validator(data)
    if not valid:
        return redirect('/menu')
    if valid:
        item = Menu.add_menu(data)
        print(item)
        print('item added')
        return redirect('/menu')

@app.route('/add_item_size', methods = ['POST'])
def add_item_size():
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        'name':request.form['name'],
        'price':request.form['price'],
        'menu_id':request.form['menu_id']
    }
    valid = Size.size_validator(data)
    if not valid:
        return redirect('/menu')
    if valid:
        item = Size.add_size(data)
        print(item)
        print('Size added')
        return redirect('/menu')

@app.route('/item/<int:id>')
def show_edit_menu(id):
    if 'employee_id' not in session:
            return redirect('/logout')
    data = {
        'product_id' : id
    }
    user_data = {
        'id':session['employee_id']
    }
    return render_template('edit_menu.html', item = Menu.show_single_item(data),show_items = Menu.get_all(), employees = Employee.show_single_user(user_data))

@app.route('/edit_item/<int:id>', methods = ['GET','POST'])
def edit_item(id):
    if 'employee_id' not in session:
        return redirect('/logout')

    data = {
        'id': id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'category':request.form['category']
    }
    valid = Menu.edit_menu_validator(data)
    if not valid:
        return redirect(f'/item/{id}')
    if valid:
        item = Menu.edit_menu(data)
        print(item)
        print('item edited')
        flash('Item Updated',category = 'success')
        return redirect('/menu')

@app.route('/edit_item_size/<int:id>',methods = ['POST'])
def edit_item_size_and_price(id):
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        'name':request.form['size_name'],
        'product_id':request.form['product_id'],
        'price':request.form['price']
    }
    valid = Size.size_update_validator(data)
    print(id)
    if not valid:
        return redirect(f'/item/{id}')
    print(valid)
    if valid:
        item = Size.edit_size(data)
        print(item)
        flash('Item Updated',category = 'success')
        return redirect('/menu')

@app.route('/show_price',methods = ['POST'])
def show_price(): 
    data = request.get_json()
    print(data)
    results = Size.show_single_size_and_product(data)
    price= results.price
    product_id = results.menu_id
    return json.dumps({'price':price,'product_id': product_id}), 200, {'ContentType':'application/json'} 

@app.route('/change_item_picture/<int:id>', methods = ['POST'])
def change_picture(id):
    if 'employee_id' not in session:
        return redirect('/logout')
    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file Part')
            return redirect(f'/item/{id}')
        file = request.files['picture']
        if file.filename =='':
            flash ('Please select file')
            return redirect(f'/item/{id}')
        if file and allowed_file(file.filename):
            pics = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pics))  
    data = {
        'id': id,
        'picture' : request.files['picture'].filename
    }
    valid = Menu.edit_menu_validator_pic(data)
    if not valid:
        return redirect(f'/item/{id}')
    if valid:
        item = Menu.edit_image(data)
        print(item)
        print('item added')
        flash('Picture Updated', category = 'success')
        return redirect('/menu')
    





