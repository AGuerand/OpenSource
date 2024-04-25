from flask import Flask, render_template, request, url_for, flash, redirect, Response, session
from security import verify_password
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyotp
from double_auth import send_email
import sqlite3
import os
from monitor import Monitor
from database import *
from right import perm
from integrity import use_integrity
import threading
import queue


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

update_queue = queue.Queue()

def print_database(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Retrieve all rows from file_paths table
    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()

    print("ID\tPathname")
    for row in rows:
        print(f"{row[0]}\t{row[1]}")  # Print ID and pathname for each row

    conn.close()  # Close database connection

    # Return the database content
    return rows

def main():
    # Check if the database file exists, if not, create it
    if not os.path.exists("path.db"):
        Create_Database("path.db")

    # Get paths from the database
    paths = get_path("path.db")

    # Start monitoring thread
    monitor_thread = threading.Thread(target=Monitor, args=("path.db", update_queue))
    monitor_thread.daemon = True
    monitor_thread.start()

def double_auth(sender_email, sender_password, receiver_email):
    secret = pyotp.random_base32()
    otp = pyotp.TOTP(secret)
    otp_value = otp.now()

    subject = 'Email opt'
    message = f"opt : {otp_value}"

    send_email(sender_email, sender_password, receiver_email, subject, message)
    print(otp_value)

    return secret, otp_value

@app.route('/')
def index():
    # Check if user is logged in
    if 'logged_in' in session and session['logged_in']:
        # User is logged in, display the index page
        main()
        database_content = print_database("path.db")
        return render_template('index.html', database_content=database_content)
    else:
        # User is not logged in, redirect to the password page
        return redirect(url_for('login'))

@app.route('/change_permissions', methods=['POST'])
def change_permissions():
    if request.method == 'POST':
        chemin = request.form['chemin']
        user = int(request.form['user'])
        group = int(request.form['group'])
        other = int(request.form['other'])
        
        conn = sqlite3.connect("path.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM file_paths WHERE id=?", (chemin,))
        chemin_exist = cursor.fetchone()
        if chemin_exist:
            cursor.execute("SELECT pathname FROM file_paths WHERE id=?", (chemin,))
            chemin = cursor.fetchone()
            perm(chemin[0], user, group, other)
            flash('Permissions changed successfully.', 'success')
        else:
            flash('Invalid ID.', 'error')

        conn.close()

    return redirect(url_for('index'))

@app.route('/add_path', methods=['POST'])
def add_path():
    if request.method == 'POST':
        path = request.form['path']
        Insert_Path("path.db", path, update_queue)
        flash('Path added successfully.', 'success')

    return redirect(url_for('index'))

@app.route('/delete_path', methods=['POST'])
def delete_path():
    if request.method == 'POST':
        path = request.form['path']
        Delete_Path("path.db", path, update_queue)
        flash('Path deleted successfully.', 'success')

    return redirect(url_for('index'))

@app.route('/check_integrity')
def check_integrity():
    use_integrity()
    flash('Integrity checked successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/page')
def page():
    return render_template('page.html')

# Route to logout
@app.route('/logout')
def logout():
    # Clear the session to logout the user
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verify password
        if verify_password("password.txt", request.form['password']):
            # Generate OTP and send email
            sender_email = 'nova77230@gmail.com'
            sender_password = 'yfjq hsmj dwqp lcjx'
            receiver_email = 'anthony.guerand2001@gmail.com'
            secret, otp_value = double_auth(sender_email, sender_password, receiver_email)
            # Store secret in session for verification later
            session['secret'] = secret
            flash('OTP sent to your email. Please check and enter it below.', 'success')
            return redirect(url_for('auth'))  # Redirect to the authentication page
        else:
            flash('Invalid password.', 'error')
    return render_template('login.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        user_token = request.form.get('token')  # Get the user-provided token
        secret = session.get('secret')  # Retrieve the secret from the session
        if secret:
            otp = pyotp.TOTP(secret)
            if otp.verify(user_token):
                session['logged_in'] = True
                flash('Authentication successful.', 'success')
                return redirect(url_for('index'))  # Redirect to the index page upon successful authentication
            else:
                flash('Authentication failed. Please try again.', 'error')
        else:
            flash('Authentication session expired. Please login again.', 'error')
            return redirect(url_for('login'))  # Redirect to the login page if no secret found in the session
    return render_template('auth.html')



if __name__ == '__main__':
    app.run(debug=True)