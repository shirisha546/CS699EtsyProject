import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from passlib.hash import bcrypt_sha256

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'etsydb'
app.secret_key = 'your_secret_key'  # Change this to your desired secret key

mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''  # Initialize an empty message variable
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form data
        if not firstname or not lastname or not email or not password or not confirm_password:
            msg = "All fields are required"
        elif password != confirm_password:
            msg = "Passwords do not match"
        else:
            # Check if user already exists
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM customers WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user:
                msg = "User already exists"
            else:
                # Hash password

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Insert new user into the database
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO customers (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                            (firstname, lastname, email, hashed_password))
                mysql.connection.commit()
                cur.close()

                # Registration successful
                msg = "Registration successful. Please log in."

                # Redirect to login page
                return redirect(url_for('login'))

    return render_template('registration.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''  # Initialize an empty message variable
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from database
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.check_password_hash(user['password'], password):
                # Successful login
                session['user_id'] = user['id']
                session['email'] = user['email']

                return redirect(url_for('customer_homepage'))
            else:
                msg = "Incorrect Username or Email"


        else:
            msg = "User Not Found"

    return render_template('login.html', msg=msg)


@app.route('/customer_homepage')
def customer_homepage():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT firstname, lastname FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            return render_template('customer_homepage.html', user=user)
        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
