from flask import render_template, request, Blueprint, jsonify, abort, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from product_database import get_db_connection, is_employee

staff = Blueprint('staff', __name__)


@staff.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    staff_id = data['staff_id']
    if not is_employee(staff_id):
        abort(403, description="Access denied: Only employees can add stock.")
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

@staff.route('/delete_product', methods=['DELETE'])
def delete_product():
    data = request.json
    staff_id = data['staff_id']
    if not is_employee(staff_id):
        abort(403, description="Access denied: Only employees can add stock.")
    product_id = request.args.get('product_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product WHERE ProductID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product deleted", 'success')
    return redirect(url_for('main.home'))

@staff.route('/modify_product', methods=['PUT'])
def modify_product():
    data = request.json
    staff_id = data['staff_id']
    if not is_employee(staff_id):
        abort(403, description="Access denied: Only employees can add stock.")
    product_id = data['product_id']
    new_name = data['new_name']
    new_category = data['new_category']
    new_type = data['new_type']
    new_brand = data['new_brand']
    new_size = data['new_size']
    new_description = data['new_description']
    new_price = data['new_price']
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
    """, (new_name, new_category, new_type, new_brand, new_size, new_description, new_price, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product modified", 'success')
    return redirect(url_for('main.home'))

@staff.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.json
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
