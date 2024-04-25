from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def login_redirect():
    return redirect(url_for('authentification'))

@app.route('/doubleAuthentification')
def double_authentification():
    return render_template('doubleAuthentification/doubleAuthentification.html')

if __name__ == '__main__':
    app.run(debug=True)
