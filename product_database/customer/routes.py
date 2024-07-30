from flask import render_template, request, Blueprint, jsonify, abort, redirect, url_for, flash, make_response
import psycopg2
import json
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from product_database import get_db_connection

customer = Blueprint('customer', __name__)


@customer.route('/search_product', methods=['GET', 'POST'])
def search_product():
    # product_name = request.args.get('product_name')
    product_name = request.form.get('product_name')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Product WHERE Name LIKE %s",
                   ('%' + product_name + '%',))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    # products = jsonify(products)
    return render_template('search_results.html', products=products, title='Search Product', search_query=product_name)


@customer.route('/shopping_cart', methods=['GET'])
def shopping_cart():
    # conn = get_db_connection
    # cursor = conn.cursor(cursor_factory=RealDictCursor)
    cart = request.cookies.get('cart')
    if not cart:
        flash("Cart is empty", 'danger')
        return redirect(request.referrer)
    cartObject = json.loads(cart)
    return render_template('shoppingcart.html', cart=cartObject)


@customer.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    quantity = request.form.get('quantity')
    cartEntry = {
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity
    }

    cookie = request.cookies.get('cart')
    cookieJson = []
    if (cookie):
        cookieJson = json.loads(cookie)
        cookieJson["items"].append(cartEntry)
    else:
        cookieJson = {"items": [cartEntry]}

    cookie = jsonify(cookieJson).get_data(as_text=True)
    # Store in Cookie
    response = make_response(redirect('/'))
    response.set_cookie("cart", value=cookie)
    return response
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("""
    #     SELECT OrderID FROM CustomerOrder
    #     WHERE CustomerID = %s AND Status = 'pending' LIMIT 1
    # """, (customer_id,))
    # order = cursor.fetchone()
    # if order is None:
    #     cursor.execute("""
    #         INSERT INTO CustomerOrder (CustomerID, OrderDate, Status)
    #         VALUES (%s, NOW(), 'pending') RETURNING OrderID
    #     """, (customer_id,))
    #     order_id = cursor.fetchone()[0]
    # else:
    #     order_id = order[0]

    # cursor.execute("""
    #     INSERT INTO OrderProduct (OrderID, ProductID, Quantity)
    #     VALUES (%s, %s, %s)
    #     ON CONFLICT (OrderID, ProductID)
    #     DO UPDATE SET Quantity = OrderProduct.Quantity + EXCLUDED.Quantity
    # """, (order_id, product_id, quantity))
    # conn.commit()
    # cursor.close()
    # conn.close()
    # flash("Product added to cart", 'success')
    # return redirect(url_for('main.home'))


@customer.route('/place_order', methods=['POST'])
def place_order():
    conn = get_db_connection()
    cursor = conn.cursor()
    cartdata = request.cookies.get('cart')
    if not cartdata:
        flash("Cart is empty", 'danger')
        return redirect(request.referrer)
    cartdata = json.loads(cartdata)

    data = request.form
    if not data:
        flash("Data is empty", 'danger')
        return redirect(request.referrer)

    customer_id = data['customer_id']

    cursor.execute("""
        SELECT CreditCardID FROM CreditCard
        WHERE CustomerID = %s
        LIMIT 1
    """, (customer_id,))
    card_result = cursor.fetchone()

    if not card_result:
        flash("No credit card found for the customer", 'danger')
        conn.close()
        return redirect(request.referrer)

    card_id = card_result[0]

    cursor.execute("""
        UPDATE CustomerOrder
        SET Status = 'placed', CreditCardID = %s, OrderDate = NOW()
        WHERE CustomerID = %s AND Status = 'pending'
    """, (card_id, customer_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Order placed", 'success')
    return redirect(url_for('main.home'))


@customer.route('/credit_card/<int:card_id>', methods=['GET'])
def credit_card(card_id):
    # product_name = request.args.get('product_name')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # only view for customer 1 for now
    cursor.execute(
        "SELECT * FROM creditcard WHERE customerid = %s", (card_id,))
    cards = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('creditcard.html', cards=cards)


@customer.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    data = request.form
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


@customer.route('/delete_credit_card/<int:card_id>', methods=['POST', 'GET'])
def delete_credit_card(card_id):
    # credit_card_id = request.args.get('credit_card_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM CreditCard WHERE CreditCardID = %s", (card_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Credit card deleted", 'success')
    return redirect(url_for('main.home'))


@customer.route('/modify_credit_card', methods=['POST'])
def modify_credit_card():
    data = request.form
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
