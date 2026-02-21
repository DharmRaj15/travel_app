import os
from flask import current_app, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import cast,Date
from app.models import Booking, schedules, seats, user, Vehicles, Route
from app import db
from datetime import datetime


def register_routes(app):

    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'name' not in session:
                flash("Please log in to access this page.", "warning")
                next_url = request.url
                return redirect(url_for('login', next=next_url))
            return f(*args, **kwargs)
        return decorated_function
    
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
                flash("Welcome back!", "success")
                # If a 'next' destination exists, go there; otherwise, go home
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                flash("Invalid credentials, please try again.", "danger")
                return redirect(url_for('login'))
        elif request.method == 'GET':
            return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('name', None)
        session.pop('user_id', None)  # Remove user ID from session
        flash("Successfully logged out. See you soon!", "danger") # 'success' maps to CSS class
        return redirect(url_for('index'))
        
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
    
    #@app.route('/seatlayout')
    #def seatlayout():
    #    return render_template('seatlyout.html')

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
    @login_required
    def confirm_booking(schedule_id):
        # 1. Get the string "1,2,5" from the form
        seats_string = request.form.get('selected_seats_list')
        created_bookings = [] # List to hold our new booking objects
        if not seats_string:
           return redirect(url_for('seatlyout', schedule_id=schedule_id))
        # 2. Convert string to list of integers [1, 2, 5]
        seat_list = [int(s) for s in seats_string.split(',')]

        for seat_no in seat_list:
            # 1. Check if the seat is already booked for this schedule
            existing_booking = Booking.query.filter_by(
                schedule_id=schedule_id,
                seat_id=seat_no
        ).first()
            
        if existing_booking:
            # If the seat is taken, stop and inform the user
            flash(f"Seat {seat_no} was just booked by someone else! Please choose another.", "danger")
            return redirect(url_for('seatlayout', schedule_id=schedule_id))
        
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
                created_bookings.append(new_booking) # Keep track of the object
                # 4. Save all rows at once
            
            db.session.commit()
            # Pass the booking IDs to the success page
            new_ids = [str(b.booking_id) for b in created_bookings]
            ids_param = ",".join(new_ids)
            return redirect(url_for('booking_success', ids=ids_param))
        except Exception as e:
                db.session.rollback()
                # Print the error to your terminal so you can see why it's failing!
                print(f"DATABASE ERROR: {e}")
                return f"An error occurred while processing your booking. Please try again later. Error: {e}", 500


    @app.route('/booking_success/<string:ids>', methods=['GET'])
    def booking_success(ids):
        ids_str = str(ids)
        if not ids_str:
            return redirect(url_for('index'))
        # Convert "10,11,12" back to [10, 11, 12]
        booking_ids = [int(i) for i in ids_str.split(',')]
        # Fetch these specific bookings
        confirmed_bookings = Booking.query.filter(Booking.booking_id.in_(booking_ids)).all()
        # We can pull general trip info from the first booking in the list
        main_booking = confirmed_bookings[0]
        return render_template('bookingconfirmed.html', bookings=confirmed_bookings, main=main_booking)
    
    #seat layout route
    #@app.route('/seatlayout1/<int:schedule_id>')
    #def seatlayout1(schedule_id):
    #    schedule = schedules.query.get(schedule_id)
    #    if not schedule:
    #        flash("Schedule not found.", "danger")
    #        return redirect(url_for('index'))
    #    # Get all booked seats for this schedule
    #    booked_seats = Booking.query.filter_by(schedule_id=schedule_id).all()
    #    booked_seat_ids = [b.seat_id for b in booked_seats]
    #    return render_template('seatlyout.html', schedule=schedule, booked_seats=booked_seat_ids)
    
    @app.route('/seatlyout/<int:schedule_id>', methods=['GET', 'POST'])
    def seatlyout(schedule_id):
        if request.method == 'GET':
            schedule = schedules.query.get_or_404(schedule_id)
            # Get seats for the vehicle associated with this schedule
            all_seats = seats.query.filter_by(vehicle_id=schedule.vehicle_id).all()
            # Get IDs of seats already booked for this schedule
            booked_seats = [b.seat_id for b in Booking.query.filter_by(schedule_id=schedule_id).all()]
            return render_template('seatlyout.html', 
                                    schedule=schedule, 
                                    seats=all_seats, 
                                    booked_seats=booked_seats)
        elif request.method == 'POST':
            # Handle seat selection and booking confirmation here
            seat_list = request.form.getlist('selected_seats')
            ##return book_seats(schedule_id, seat_list)
    