import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
import logging
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


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''  # Initialize an empty message variable
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from database
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admins WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.check_password_hash(user['password'], password):
                # Successful login
                session['admin_id'] = user['admin_id']
                session['email'] = user['email']
                return redirect(url_for('admin_dashboard'))
            else:
                msg = "Incorrect Username or Email"

        else:
            msg = "User Not Found"

    return render_template('admin/admin_login.html', msg=msg)


@app.route('/admin/dashboard')
def admin_dashboard():
    msg = ''
    # Check if admin is logged in
    if 'admin_id' in session:

        # Fetch user details from the database using the session ID
        admin_id = session['admin_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT firstname, lastname FROM admins WHERE admin_id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()

        if admin:
            # Pass user details to the template
            return render_template('admin/dashboard.html', admin=admin)
        else:
            # User not found, redirect to login
            return redirect(url_for('admin_login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('admin_login'))


@app.route('/admin/manage_products')
def manage_products():
    msg = ''
    # Check if admin is logged in
    if 'admin_id' in session:

        # Fetch user details from the database using the session ID
        admin_id = session['admin_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT firstname, lastname FROM admins WHERE admin_id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()

        if admin:
            # Pass user details to the template
            products = admin_get_products()
            return render_template('admin/manage_products.html', admin=admin, products=products)
        else:
            # User not found, redirect to login
            return redirect(url_for('admin_login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('admin_login'))
@app.route('/admin/manage_offers')
def manage_offers():
    msg = ''
    # Check if admin is logged in
    if 'admin_id' in session:

        # Fetch user details from the database using the session ID
        admin_id = session['admin_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT firstname, lastname FROM admins WHERE admin_id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()

        if admin:
            # Pass user details to the template
            products = admin_get_offers()
            return render_template('admin/manage_offers.html', admin=admin, products=products)
        else:
            # User not found, redirect to login
            return redirect(url_for('admin_login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('admin_login'))


@app.route('/admin/add_products')
def add_products():
    msg = ''
    # Check if admin is logged in
    if 'admin_id' in session:

        # Fetch user details from the database using the session ID
        admin_id = session['admin_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT firstname, lastname FROM admins WHERE admin_id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()

        if admin:
            # Pass user details to the template

            return render_template('admin/add_products.html', admin=admin)
        else:
            # User not found, redirect to login
            return redirect(url_for('admin_login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('admin_login'))


# Route for adding a product
@app.route('/admin/submit_product', methods=['GET', 'POST'])
def submit_product():
    msg = ''  # Initialize an empty message variable

    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        type = request.form['type']

        image = request.files['image']

        # Validate form data
        if not name or not price or not description or not image:
            msg = "All fields are required"
        else:
            # Save image file to static/productimages folder
            if image.filename != '':
                image_path = os.path.join('static/product_images/', image.filename)
                image.save(image_path)

                # Insert product details into the database
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO products (name, price, description, category, image_path, type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, price, description, category, image.filename, type))
                mysql.connection.commit()
                cur.close()

                # Product addition successful
                # Return JavaScript code to display a message
                js_code = "alert('Product added successfully. Add another.');"
                return Response(js_code, mimetype='text/javascript')
            else:
                msg = "Adding product failed"
            # Redirect to the manage products page or any other desired page
        return redirect(url_for('add_products', msg=msg))
    return render_template('admin/add_products.html', msg=msg)


# Method to fetch products from the database
def admin_get_products():
    # Connect to the database
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch products from the 'products' table
    cur.execute("SELECT * FROM products WHERE type = 'sales'")
    products = cur.fetchall()

    cur.close()

    return products

#Method to Fetch Offers
def admin_get_offers():
    # Connect to the database
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch products from the 'products' table
    cur.execute("SELECT * FROM products WHERE type = 'offer'")
    products = cur.fetchall()

    cur.close()

    return products


# Function to fetch products based on category

def get_products_by_category(category):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM products WHERE category = %s", (category,))
        products = cur.fetchall()
        return products

    except mysql.connector.Error as err:
        print("Error:", err)
        return []

#Get products on offer

def get_products_on_offer():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM products WHERE type = 'offer'")
        products = cur.fetchall()
        return products

    except mysql.connector.Error as err:
        print("Error:", err)
        return []


@app.route('/products/<category>')
def products(category):
    # Fetch products based on category
    products = get_products_by_category(category)
    return render_template('products.html', products=products)


@app.route('/customer_products/<category>')
def customer_products(category):
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            products = get_products_by_category(category)
            return render_template('customer_products.html', products=products, user=user)
        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))
        # Fetch products based on category

@app.route('/customer_offers')
def customer_offers():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            products = get_products_on_offer()
            return render_template('customer_offers.html', products=products, user=user)
        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))
        # Fetch products based on category


def get_single_product(id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cur.fetchone()
        return product

    except mysql.connector.Error as err:
        print("Error:", err)
        return []


@app.route('/single_product/<id>')
def display_single_product(id):
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            products = get_single_product(id)
            return render_template('single_product.html', products=products, user=user)
        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))
        # Fetch products based on category


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        # Extract values from the request
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        unit_price = request.form.get('unit_price')

        # Log the received values
        print("Received values:")
        print("Customer ID:", customer_id)
        print("Product ID:", product_id)
        print("Quantity:", quantity)
        print("Unit Price:", unit_price)

        try:
            # Your database insertion code here
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                INSERT INTO purchases (customerid, productid, quantity, unitprice, status)
                VALUES (%s, %s, %s, %s, 'cart')
            """, (customer_id, product_id, quantity, unit_price))
            mysql.connection.commit()
            cur.close()
            return "Success"
        except mysql.connector.Error as err:
            print("Error:", err)
            return "Error"
    else:
        return "Method Not Allowed"


@app.route('/cart')
def cart():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                        SELECT products.name, purchases.quantity, purchases.unitprice
                        FROM purchases
                        INNER JOIN products ON purchases.productid = products.id
                        WHERE purchases.customerid = %s AND purchases.status = 'cart'
                    """, (user_id,))
            cart_items = cur.fetchall()
            cur.close()
            # Calculate total cost
            total_cost = sum(item['quantity'] * item['unitprice'] for item in cart_items)

            return render_template('cart.html', user=user, cart_items=cart_items, total_cost=total_cost)

        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))
@app.route('/checkout')
def checkout():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                        SELECT products.name, purchases.quantity, purchases.unitprice
                        FROM purchases
                        INNER JOIN products ON purchases.productid = products.id
                        WHERE purchases.customerid = %s AND purchases.status = 'cart'
                    """, (user_id,))
            cart_items = cur.fetchall()
            cur.close()
            # Calculate total cost
            total_cost = sum(item['quantity'] * item['unitprice'] for item in cart_items)

            return render_template('checkout.html', user=user, cart_items=cart_items, total_cost=total_cost)

        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))

from flask import request, jsonify

@app.route('/complete_payment', methods=['POST'])
def complete_payment():
    if request.method == 'POST':
        # Extract values from the request
        customer_id = request.form.get('customer_id')
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        total_cost = float(request.form.get('total_cost'))

        # Log the received values
        print("Received values:")
        print("Customer ID:", customer_id)
        print("Address:", address)
        print("Payment Method:", payment_method)

        try:
            # Update the purchases table to set purchase date, address, payment method, and status
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                UPDATE purchases
                SET purchasedate = NOW(), shippingaddress = %s, paymentmethod = %s, status = 'paid'
                WHERE customerid = %s AND status = 'cart'
            """, (address, payment_method, customer_id))
            mysql.connection.commit()
            cur.close()

            if total_cost >= 500:
                try:
                    # Your database insertion code here
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("""
                        INSERT INTO loyaltypoints (customerid, points_earned, date_earned)
                        VALUES (%s,10, NOW())
                    """, (customer_id,))
                    mysql.connection.commit()
                    cur.close()
                    return "Success"
                except mysql.connector.Error as err:
                    print("Error:", err)
                    return "Error"

            else:
                return "No points earned"
            return jsonify({'message': 'Payment completed successfully!'})
        except mysql.connector.Error as err:
            print("Error:", err)
            return jsonify({'error': 'Error completing payment'}), 500
    else:
        return "Method Not Allowed"

@app.route('/customer_purchases')
def customer_purchases():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                        SELECT products.name, purchases.quantity, purchases.unitprice, purchases.shippingaddress, purchases.paymentmethod,
                        purchases.purchasedate, purchases.status
                        FROM purchases
                        INNER JOIN products ON purchases.productid = products.id
                        WHERE purchases.customerid = %s AND purchases.status != 'cart'
                    """, (user_id,))
            purchases = cur.fetchall()
            cur.close()


            return render_template('customer_purchases.html', user=user, purchases=purchases)

        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))

@app.route('/view_loyalty_points')
def view_loyalty_points():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                        SELECT * FROM loyaltypoints WHERE customerid = %s AND status = 'active'
                    """, (user_id,))
            points = cur.fetchall()
            cur.close()

            total_points = sum(item['points_earned'] for item in points)

            #All time points

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""
                                    SELECT * FROM loyaltypoints WHERE customerid = %s
                                """, (user_id,))
            all_points = cursor.fetchall()
            cursor.close()

            every_alltimepoints = all_points

            alltime_points = sum(item['points_earned'] for item in all_points)
            loyalty_level = None
            if alltime_points < 100:
                loyalty_level = 0
            elif 100 <= alltime_points < 200:
                loyalty_level = 1
            elif 200 <= alltime_points < 250:
                loyalty_level = 2
            else:
                loyalty_level = "Gold Customer"  # You can adjust this label as needed


            return render_template('myloyaltypoints.html', user=user, points = points,
                                   total_points=total_points, alltime_points=alltime_points, loyalty_level=loyalty_level, every_alltimepoints = every_alltimepoints)

        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))

@app.route('/view_notifications')
def view_notifications():
    if 'user_id' in session:
        # Fetch user details from the database using the session ID
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM customers WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user details to the template
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                        SELECT * FROM loyaltypoints WHERE customerid = %s AND display_status = 'new' ORDER BY date_earned DESC
                    """, (user_id,))
            points = cur.fetchall()
            cur.close()

            return render_template('view_notifications.html', user=user, points = points)

        else:
            # User not found, redirect to login
            return redirect(url_for('login'))
    else:
        # User not logged in, redirect to login
        return redirect(url_for('login'))

@app.route('/admin_logout')
def admin_logout():
    # Clear the session
    session.pop('admin_id', None)
    session.pop('email', None)
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
