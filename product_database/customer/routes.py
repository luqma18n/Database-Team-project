from flask import render_template, request, Blueprint, jsonify, abort, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from product_database import get_db_connection

customer = Blueprint('customer', __name__)


@customer.route('/search_product', methods=['GET'])
def search_product():
    product_name = request.args.get('product_name')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Product WHERE Name LIKE %s", ('%' + product_name + '%',))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@customer.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    customer_id = data['customer_id']
    product_id = data['product_id']
    quantity = data['quantity']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT OrderID FROM CustomerOrder 
        WHERE CustomerID = %s AND Status = 'pending' LIMIT 1
    """, (customer_id,))
    order = cursor.fetchone()
    if order is None:
        cursor.execute("""
            INSERT INTO CustomerOrder (CustomerID, OrderDate, Status)
            VALUES (%s, NOW(), 'pending') RETURNING OrderID
        """, (customer_id,))
        order_id = cursor.fetchone()[0]
    else:
        order_id = order[0]

    cursor.execute("""
        INSERT INTO OrderProduct (OrderID, ProductID, Quantity) 
        VALUES (%s, %s, %s)
        ON CONFLICT (OrderID, ProductID) 
        DO UPDATE SET Quantity = OrderProduct.Quantity + EXCLUDED.Quantity
    """, (order_id, product_id, quantity))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product added to cart", 'success')
    return redirect(url_for('main.home'))

@customer.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    customer_id = data['customer_id']
    credit_card_id = data['credit_card_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CustomerOrder 
        SET Status = 'placed', CreditCardID = %s, OrderDate = NOW()
        WHERE CustomerID = %s AND Status = 'pending'
    """, (credit_card_id, customer_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Order placed", 'success')
    return redirect(url_for('main.home'))

@customer.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    data = request.json
    customer_id = data['customer_id']
    card_number = data['card_number']
    expiration_date = data['expiration_date']
    security_code = data['security_code']
    payment_address_id = data['payment_address_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CreditCard (CustomerID, CardNumber, ExpirationDate, SecurityCode, PaymentAddressID)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer_id, card_number, expiration_date, security_code, payment_address_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Credit card added", 'success')
    return redirect(url_for('main.home'))

@customer.route('/delete_credit_card', methods=['DELETE'])
def delete_credit_card():
    credit_card_id = request.args.get('credit_card_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CreditCard WHERE CreditCardID = %s", (credit_card_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Credit card deleted", 'success')
    return redirect(url_for('main.home'))

@customer.route('/modify_credit_card', methods=['PUT'])
def modify_credit_card():
    data = request.json
    credit_card_id = data['credit_card_id']
    new_card_number = data['new_card_number']
    new_expiration_date = data['new_expiration_date']
    new_security_code = data['new_security_code']
    new_payment_address_id = data['new_payment_address_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CreditCard
        SET CardNumber = %s,
            ExpirationDate = %s,
            SecurityCode = %s,
            PaymentAddressID = %s
        WHERE CreditCardID = %s
    """, (new_card_number, new_expiration_date, new_security_code, new_payment_address_id, credit_card_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Credit card modified", 'success')
    return redirect(url_for('main.home'))

@customer.route('/add_address', methods=['POST'])
def add_address():
    data = request.json
    customer_id = data['customer_id']
    address_line1 = data['address_line1']
    address_line2 = data['address_line2']
    city = data['city']
    state = data['state']
    zip_code = data['zip_code']
    address_type = data['address_type']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Address (CustomerID, AddressLine1, AddressLine2, City, State, ZipCode, AddressType)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (customer_id, address_line1, address_line2, city, state, zip_code, address_type))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Address added", 'success')
    return redirect(url_for('main.home'))

@customer.route('/delete_address', methods=['DELETE'])
def delete_address():
    address_id = request.args.get('address_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Address WHERE AddressID = %s", (address_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Address deleted", 'success')
    return redirect(url_for('main.home'))

@customer.route('/modify_address', methods=['PUT'])
def modify_address():
    data = request.json
    address_id = data['address_id']
    new_address_line1 = data['new_address_line1']
    new_address_line2 = data['new_address_line2']
    new_city = data['new_city']
    new_state = data['new_state']
    new_zip_code = data['new_zip_code']
    new_address_type = data['new_address_type']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Address
        SET AddressLine1 = %s,
            AddressLine2 = %s,
            City = %s,
            State = %s,
            ZipCode = %s,
            AddressType = %s
        WHERE AddressID = %s
    """, (new_address_line1, new_address_line2, new_city, new_state, new_zip_code, new_address_type, address_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Address modified", 'success')
    return redirect(url_for('main.home'))
