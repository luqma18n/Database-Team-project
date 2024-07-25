from flask import render_template, request, Blueprint, jsonify, abort, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from product_database import get_db_connection, is_employee

staff = Blueprint('staff', __name__)

@staff.route('/view_product', methods=['GET', 'POST'])
def view_product():
    # product_name = request.args.get('product_name')
    product_name = request.form.get('product_name')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Product WHERE Name LIKE %s", ('%' + product_name + '%',))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    # products = jsonify(products)
    return render_template('staff_results.html', products=products, title='Search Product', search_query=product_name)

@staff.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        data = request.form
        # staff_id = data['staff_id']
        # if not is_employee(staff_id):
        #     abort(403, description="Access denied: Only employees can add stock.")
        name = data['name']
        category = data['category']
        type_ = data['type']
        brand = data['brand']
        size = data['size']
        description = data['description']
        price = data['price']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Product (Name, Category, Type, Brand, Size, Description, Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, category, type_, brand, size, description, price))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Product added", 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        return render_template('add_product.html', title='Add Product')

@staff.route('/delete_product/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
    # staff_id = data['staff_id']
    # if not is_employee(staff_id):
    #     abort(403, description="Access denied: Only employees can add stock.")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product WHERE ProductID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product deleted", 'success')
    return redirect(url_for('main.home'))

@staff.route('/modify_product', methods=['POST'])
def modify_product():
    data = request.form
    # staff_id = data['staff_id']
    # if not is_employee(staff_id):
    #     abort(403, description="Access denied: Only employees can modify stock.")
    product_id = data['product_id']
    name = data['name']
    category = data['category']
    type_ = data['type']
    brand = data['brand']
    size = data['size']
    description = data['description']
    price = data['price']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Product
        SET Name = %s,
            Category = %s,
            Type = %s,
            Brand = %s,
            Size = %s,
            Description = %s,
            Price = %s
        WHERE ProductID = %s
    """, (name, category, type_, brand, size, description, price, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product modified", 'success')
    return redirect(url_for('main.home'))

@staff.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.form
    staff_id = data['staff_id']
    if not is_employee(staff_id):
        abort(403, description="Access denied: Only employees can add stock.")
    product_id = data['product_id']
    warehouse_id = data['warehouse_id']
    quantity = data['quantity']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Stock (ProductID, WarehouseID, Quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (ProductID, WarehouseID) 
        DO UPDATE SET Quantity = Stock.Quantity + EXCLUDED.Quantity
    """, (product_id, warehouse_id, quantity))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Stock added", 'success')
    return redirect(url_for('main.home'))
