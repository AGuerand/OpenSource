from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def authentification():
    return render_template('Authentification.html')

@app.route('/doubleAuthentification')
def double_authentification():
    return render_template('doubleAuthentification.html')

@app.route('/login', methods=['POST'])
def login():
    # Ici, vous pouvez ajouter le code pour vérifier l'authentification de l'utilisateur
    # Si l'authentification réussit, vous pouvez rediriger vers la page de double authentification
    return redirect(url_for('double_authentification'))

if __name__ == '__main__':
    app.run(debug=True)