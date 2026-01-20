from app import db

class user(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    phone = db.Column(db.String(20),  nullable=True)
    dbo = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    

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
    
