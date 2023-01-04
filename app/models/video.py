from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    release_date = db.Column(db.Datetime)
    total_inventory = db.Column(db.Integer)