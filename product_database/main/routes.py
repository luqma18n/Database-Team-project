from flask import render_template, request, Blueprint, jsonify, abort, redirect, url_for, flash, make_response
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json
from dotenv import load_dotenv
from product_database import get_db_connection, is_employee

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def home():
    #staff = is_employee(1)
    cookie = request.cookies.get('status')
    staff = True if cookie == "staff" else False
    return render_template('home.html', title='Home', staff=staff)

@main.route('/set_status', methods=['GET'])
def set_status():
    cookie = request.cookies.get('status')
    if(cookie == "staff"):
        response = make_response(redirect('/'))
        response.set_cookie("status", value="customer")
        return response
    elif(cookie == "customer"):
        response = make_response(redirect('/'))
        response.set_cookie("status", value="staff")
        return response
    else:
        response = make_response(redirect('/'))
        response.set_cookie("status", value="staff")
        return response