from flask import Flask, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

def is_employee(staff_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS (SELECT 1 FROM StaffMember WHERE StaffID = %s)", (staff_id,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result


# Customer routes

@app.route('/search_product', methods=['GET'])
def search_product():
    product_name = request.args.get('product_name')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Product WHERE Name LIKE %s", ('%' + product_name + '%',))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route('/add_to_cart', methods=['POST'])
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
    return jsonify({"message": "Product added to cart"})

@app.route('/place_order', methods=['POST'])
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
    return jsonify({"message": "Order placed"})

@app.route('/add_credit_card', methods=['POST'])
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
    return jsonify({"message": "Credit card added"})

@app.route('/delete_credit_card', methods=['DELETE'])
def delete_credit_card():
    credit_card_id = request.args.get('credit_card_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CreditCard WHERE CreditCardID = %s", (credit_card_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Credit card deleted"})

@app.route('/modify_credit_card', methods=['PUT'])
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
    return jsonify({"message": "Credit card modified"})

@app.route('/add_address', methods=['POST'])
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
    return jsonify({"message": "Address added"})

@app.route('/delete_address', methods=['DELETE'])
def delete_address():
    address_id = request.args.get('address_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Address WHERE AddressID = %s", (address_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Address deleted"})

@app.route('/modify_address', methods=['PUT'])
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
    return jsonify({"message": "Address modified"})

# Staff routes

@app.route('/add_product', methods=['POST'])
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
    return jsonify({"message": "Product added"})

@app.route('/delete_product', methods=['DELETE'])
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
    return jsonify({"message": "Product deleted"})

@app.route('/modify_product', methods=['PUT'])
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
    return jsonify({"message": "Product modified"})

@app.route('/add_stock', methods=['POST'])
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
    return jsonify({"message": "Stock added"})

if __name__ == '__main__':
    app.run(debug=True)
