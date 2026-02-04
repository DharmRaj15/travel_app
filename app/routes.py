import os
from flask import current_app, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import cast,Date
from app.models import Booking, schedules, user, Vehicles, Route
from app import db
from datetime import datetime


def register_routes(app):
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        vehicles_list = Vehicles.query.all()
        routes_list = Route.query.all()

        # Initialize result as None
        route_obj = None

        if request.method == 'POST':
            pickup = request.form.get('pickup')
            destination = request.form.get('destination')
            travel_date = request.form.get('traveldate')
            bustype = request.form.get('bustype')
           
            bus_searchQuery = db.session.query(schedules, Route, Vehicles).join(Route).join(Vehicles).filter(
                Route.origin == pickup,
                Route.destination == destination,
                cast(schedules.departure_time, Date) == travel_date,
                Vehicles.vehicle_id == bustype)
            route_obj = bus_searchQuery.all()
            return render_template('index.html', bus = vehicles_list, routes = routes_list, search_result=route_obj)
        
        elif request.method == 'GET':
            return render_template('index.html', bus = vehicles_list, routes = routes_list)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            username = session['name']
            all_users = user.query.all()
            return render_template('register.html',users=all_users,username=username)
        elif request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form.get('phone')
            dbo = request.form.get('dbo')
            gender = request.form.get('gender')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            terms = request.form.get('terms')
            
            # Validate password match
            if password != confirm_password:
                return "Passwords do not match!", 400
            
            new_user = user(
                full_name=full_name, 
                email=email, 
                phone=phone, 
                dbo=dbo, 
                gender=gender,
                password=password,
                confirm_password=confirm_password,
                terms=bool(terms)
            )
            db.session.add(new_user)
            db.session.commit()
            return f"User {full_name} registered successfully!"

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form.get('password')
            user_obj = user.query.filter_by(email=email, password=password).first()
            if user_obj:
                session['name'] = user_obj.full_name
                session['user_id'] = user_obj.id  # Store user ID in session
                return render_template('index.html')
            else:
                return "Invalid credentials, please try again.", 401
        elif request.method == 'GET':
            return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('name', None)
        return render_template('index.html')
        
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    

    @app.route('/debug-db')
    def debug_db():
        return f"The app is currently using: {current_app.config['SQLALCHEMY_DATABASE_URI']}"
    
    @app.route('/data', methods=['GET'])
    def data():
        abo = user.query.all()
        return str(abo)    
    @app.route('/mytickets')
    def mytickets():
        return render_template('mytickets.html')
    
    @app.route('/other')
    def other():
        return render_template('other.html')
    
    @app.route('/seatlayout')
    def seatlayout():
        return render_template('seatlyout.html')

    @app.route('/login1', methods=['GET', 'POST'])
    def login1():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            # Add your login logic here
            return "Login functionality coming soon!"
    
    @app.route('/set-cookie')
    def set_cookie():
        return "Cookie set!"
    
    @app.route('/get-cookie')
    def get_cookie():
        return "Get cookie functionality coming soon!"
    
    @app.route('/delete-cookie')
    def delete_cookie():
        return "Cookie deleted!"
    
    ### bookings routes ###
    @app.route('/confirm_booking/<int:schedule_id>', methods=['POST', 'GET'])
    def confirm_booking(schedule_id):
        # 1. Get the string "1,2,5" from the form
        seats_string = request.form.get('selected_seats_list')
        if not seats_string:
           return redirect(url_for('seatlayout', schedule_id=schedule_id))
        # 2. Convert string to list of integers [1, 2, 5]
        seat_list = [int(s) for s in seats_string.split(',')]
        try:
            for seat_no in seat_list:
                # 3. Create a new row for every seat selected
                new_booking = Booking(
                    schedule_id=schedule_id,
                    user_id=session.get('user_id'), # Assuming user_id is stored in session
                    seat_id=seat_no,
                    status='Confirmed'
                )
                db.session.add(new_booking)
                # 4. Save all rows at once
                db.session.commit()
            return redirect(url_for('my_bookings'))
        except Exception as e:
                db.session.rollback()
                # Print the error to your terminal so you can see why it's failing!
                print(f"DATABASE ERROR: {e}")
                return f"An error occurred while processing your booking. Please try again later. Error: {e}", 500