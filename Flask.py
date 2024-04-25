from flask import Flask, render_template, request, url_for, flash, redirect, Response, session
from security import verify_password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verify password
        if verify_password("password.txt", request.form['password']):
            # Store user's login status in session
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid password.')
    return render_template('login.html', message='')

@app.route('/')
def index():
    # Check if user is logged in
    if 'logged_in' in session and session['logged_in']:
        # User is logged in, display the index page
        return render_template('index.html')
    else:
        # User is not logged in, redirect to the password page
        return redirect(url_for('login'))

@app.route('/page')
def page():
    return render_template('page.html')



# Route to logout
@app.route('/logout')
def logout():
    # Clear the session to logout the user
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)