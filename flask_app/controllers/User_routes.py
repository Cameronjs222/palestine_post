#user login in routes
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.User_models import User

@app.route('/login')
def login_and_reg():
    return render_template('login.html')

@app.route('/validate_login', methods=['POST'])
def validate_login():
    if not User.validate_login(request.form):
        return redirect('/login')
    
    user = User.get_user_by_username(request.form)
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    User.create_user(request.form)
    return redirect('/admin')
    

@app.route('/download', methods=['POST'])
def download():
    User.read_and_save_to_database(request.form['dataset'])
    return redirect('/admin')