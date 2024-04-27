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
import logging
from logging.handlers import RotatingFileHandler
from flask import jsonify
import time
import pwd
import grp
from get_path import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


log_file = 'flask_app.log'  
login_verif = False

file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


app.logger.addHandler(file_handler)


app.logger.setLevel(logging.INFO)  


werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.disabled = True

update_queue = queue.Queue()



def print_database(database_name):
   
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    
    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()

    print("ID\tPathname")
    for row in rows:
        print(f"{row[0]}\t{row[1]}") 

    conn.close()  

   
    return rows

def main():
    
    if not os.path.exists("path.db"):
        Create_Database("path.db")

    
    paths = get_path("path.db")

    
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

@app.route('/get_log_content')
def get_log_content():
    
    with open('log.log', 'r') as file:
       log_contents = '\n'.join([line.rstrip('\n') + '\n' for line in file])

    
    return log_contents


@app.route('/')
def index():
    pathnames = get_paths('path.db')
    
    if 'logged_in' in session and session['logged_in']:
        integrity_results = use_integrity("path.db", "integrity.db")
        main()
        database_content = print_database("path.db")
        with open('log.log', 'r') as file:
            log_contents = '\n'.join([line.rstrip('\n') + '\n' for line in file])
        return render_template('index.html',database_contents=pathnames,integrity_results=integrity_results,database_content=database_content, log_contents=log_contents)
    else:
        
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
    return jsonify({'message': 'Integrity checked successfully.'})

@app.route('/page')
def page():
    return render_template('page.html')


@app.route('/logout', methods=['POST'])
def logout():
    global login_verif
    login_verif = False
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global login_verif
    if request.method == 'POST':
        
        if verify_password("password.txt", request.form['password']):
            
            sender_email = 'nova77230@gmail.com'
            sender_password = 'yfjq hsmj dwqp lcjx'
            receiver_email = 'anthony.guerand2001@gmail.com'
            secret, otp_value = double_auth(sender_email, sender_password, receiver_email)
           
            session['secret'] = secret
            flash('OTP sent to your email. Please check and enter it below.', 'success')
            login_verif = True
            return redirect(url_for('auth'))  
        else:
            flash('Invalid password.', 'error')
    return render_template('login.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    global login_verif
    if login_verif == False :
        return redirect(url_for('login')) 

    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))  
    if request.method == 'POST':
        user_token = request.form.get('token')  
        secret = session.get('secret')  
        if secret:
            otp = pyotp.TOTP(secret)
            if otp.verify(user_token):
                session['logged_in'] = True
                flash('Authentication successful.', 'success')
                return redirect(url_for('index'))  
            else:
                flash('Authentication échouée.', 'error')
                return redirect(url_for('login'))
        else:
            flash('Authentication exprirée.', 'error')
            return redirect(url_for('login'))  
    return render_template('auth.html')

@app.route('/update_integrity', methods=['POST'])
def update_integrity():
    integrity_results = use_integrity("path.db", "integrity.db")
    return jsonify(integrity_results)

def get_paths(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Select all pathnames from file_paths table
    cursor.execute("SELECT pathname FROM file_paths")
    paths = [row[0] for row in cursor.fetchall()]  # Fetch all pathnames and store in a list

    conn.close()  # Close database connection
    return paths 

# Function to fetch file details from the database
def get_file_details(file_path):
    file_name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    file_type = os.path.splitext(file_path)[1]
    last_modified = os.path.getmtime(file_path)  # Returns timestamp

    # Convert timestamp to a human-readable format
    last_modified_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_modified))

    file_owner = pwd.getpwuid(os.stat(file_path).st_uid).pw_name
    file_group = grp.getgrgid(os.stat(file_path).st_gid).gr_name

    return {
        'fileName': file_name,
        'size': size,
        'type': file_type,
        'lastModified': last_modified_formatted,
        'owner': file_owner,
        'group': file_group
    }



# Route to handle fetching file details
@app.route('/get_file_details')
def get_file_details_route():
    selected_file = request.args.get('file')
    if selected_file:
        file_details = get_file_details(selected_file)
        return jsonify(file_details)
    else:
        return jsonify({'error': 'No file selected'})


if __name__ == '__main__':
    app.run(debug=True)