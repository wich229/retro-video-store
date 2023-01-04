from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone_number = db.Column(db.String) 
    register_at = db.Column(db.Datetime)
    videos_checked_out_count = db.Column(db.Integer)


