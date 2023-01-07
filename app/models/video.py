from app import db
from datetime import datetime, date

class Video(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="rental", back_populates="videos")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
    
    @classmethod
    def from_dict(cls, data):
        pass
    
    
    # available_inventory is a function:
    # total will be video.total_inventory - vedio_id with check_out status amount
    # + vedio_id with check_in status amount
    def available_inventory(id):
        pass