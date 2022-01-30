from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return 

@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
        return render_template("sign_up.html")
 