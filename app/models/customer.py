from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
