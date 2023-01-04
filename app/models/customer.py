from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    postal_code = db.Column(db.Varchar(10)) # 10 or 5?
    phone_number = db.Column(db.Varchar(20)) # ??
    register_at = db.Column(db.Datetime)
    videos_checked_out_count = db.Column(db.Integer)


