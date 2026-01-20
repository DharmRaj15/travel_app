import os
from flask import current_app, jsonify, render_template, request
from models import user
from datetime import datetime

def register_routes(app,db):
    
    @app.route('/')
    def index():
        all_users = user.query.all()
        return  str(all_users)

    @app.route('/register', methods=['GET', 'POST'])
    def users():
        if request.method == 'GET':
            all_users = user.query.all()
            return render_template('register.html',users=all_users)
        elif request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form.get('phone')
            dbo = request.form.get('dbo')
            gender = request.form.get('gender')
            new_user = user(
                full_name=full_name, 
                email=email, 
                phone=phone, 
                dbo=dbo, 
                gender=gender
            )
            db.session.add(new_user)
            db.session.commit()
            return f"User {full_name} added successfully!"
    
    
    @app.route('/debug-db')
    def debug_db():
        return f"The app is currently using: {current_app.config['SQLALCHEMY_DATABASE_URI']}"
    
    @app.route('/data', methods=['GET'])
    def data():
        abo = user.query.all()
        return str(abo)
    
        
