from flask import Flask, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

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


def create_app():
    app = Flask(__name__)

    from product_database.staff.routes import staff
    from product_database.customer.routes import customer
    from product_database.main.routes import main

    app.secret_key = os.getenv('SECRET_KEY')
    app.register_blueprint(staff)
    app.register_blueprint(customer)
    app.register_blueprint(main)

    return app