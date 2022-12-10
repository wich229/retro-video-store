from app import db

class Customer(db.Model):
    __tablename__ = "customer"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    register_at = db.Column(db.DateTime)
    