from datetime import datetime
from app import db


class user(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    phone = db.Column(db.String(20),  nullable=True)
    dbo = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(128), nullable=True)
    confirm_password = db.Column(db.String(128), nullable=True)
    terms = db.Column(db.Boolean, nullable=True)
    

    def __repr__(self):
        return f'<register {self.full_name}>'


class Vehicles(db.Model):
    __tablename__ = 'Vehicles'
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_number = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Vehicles {self.vehicle_number}>'
    
class Route(db.Model):
    __tablename__ = 'Routes'
    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin = db.Column(db.String(80), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    estimated_time = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        # return f'<Routes {self.origin} to {self.destination}>'
        return f'<Routes {self.route_id}>'
    
class schedules(db.Model):
    __tablename__ = 'Schedules'
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicles.vehicle_id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('Routes.route_id'), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    arrival_time = db.Column(db.String(20), nullable=False)

    vehicle = db.relationship('Vehicles', backref=db.backref('schedules', lazy=True))
    route = db.relationship('Route', backref=db.backref('schedules', lazy=True))

    def __repr__(self):
        return f'<Schedules Vehicle {self.vehicle_id} on Route {self.route_id}>'
    
class Booking(db.Model):
    __tablename__ = 'Bookings'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('Schedules.schedule_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False)
    seat_id = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    schedule = db.relationship('schedules', backref=db.backref('bookings', lazy=True))
    user = db.relationship('user', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.booking_id} for Schedule {self.schedule_id}>'
    
class seats(db.Model):
    __tablename__ = 'Seats'
    seat_id = db.Column(db.String(10), primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicles.vehicle_id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    vehicle = db.relationship('Vehicles', backref=db.backref('seats', lazy=True))

    def __repr__(self):
        return f'<Seats {self.seat_id} in Vehicle {self.vehicle_id}>'