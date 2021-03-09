from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#Bootstrap işlemi

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            password = generate_password_hash(form['password'])
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO employee(name, age, password) VALUES(%s, %s, %s)", (name, age, password))
            mysql.connection.commit()
        except Exception as ex:
            return ex
    
    return render_template('index.html') # Get durumunda çalışacak bu satır

@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM employee")

    if result > 0:
        data = cur.fetchall()
        return render_template('employees.html', employees = data)

@app.route('/static')
def static_image():
    return render_template('static.html')