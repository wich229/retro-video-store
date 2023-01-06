from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.relationship('')


    """"customer_id": 122581016,
    "video_id": 235040983,
    "due_date": "2020-06-31",
    "videos_checked_out_count": 2,
    "available_inventory": 5"""
