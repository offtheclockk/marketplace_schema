from flask_app.config.mysqlconnection import query_db
from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import product
from flask_app.models import user, arrangement
DATABASE = "floral_schema"

@app.route('/product')
def one_product():
    print("***************", session['arrangement_id'])
    if 'uuid' in session:
        id = {
            'id': session['uuid']
        }
        data = {
            'user': user.User.select(data = id),
            'arrangement': arrangement.Arrangement.select(data={'id':session['arrangement_id']})[0]
        }
        return render_template('product.html', **data)
    else:
        data = {
            'arrangement': arrangement.Arrangement.select(data={'id':session['arrangement_id']})[0]
        }
        return render_template('product.html', **data)

@app.route("/products", methods=["POST"])
def products():
    session['arrangement_id'] = request.form['id']
    print("ID***************", request.form['id'])
    return redirect(f'/product')

@app.route('/products/all')
def all_products():
    if 'uuid' in session:
        id = {
            'id': session['uuid']
        }
        data = {
            'user': user.User.select(data=id),
            'arrangements': arrangement.Arrangement.select(type='size', data={'size': 'Deluxe'})
        }
        return render_template('products.html', **data)
    else:
        data = {
            'arrangements': arrangement.Arrangement.select(type='size', data={'size': 'Deluxe'})
        }
        return render_template('products.html', **data)
#notdone
# @app.route('/search/<string:name>')
# def search_dropdown(name):
#     print('name*****************************', name)
#     msg = {
#         'status': 200
#     }
#     # product_list = {}
#     product_data = {
#         'name': name+'%'
#     }
#     print (f"{'product_data':*^40}", product_data['name'])
#     products = product.Product.search_products(data=product_data)
#     print('products****************************',products)
#     if products:
#         return jsonify(msg)
#     else:
#         return jsonify(msg)

@app.route('/search/<name>')
def filter_users(name):
    query = "SELECT name FROM products WHERE products.name LIKE %(name)s LIMIT 5;"
    results = query_db(query,{"name":name+"%"})
    return jsonify(results)