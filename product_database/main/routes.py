from flask import render_template, request, Blueprint, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from product_database import get_db_connection, is_employee

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def home():
    #staff = is_employee(1)
    staff = False
    return render_template('home.html', title='Home', staff=staff)