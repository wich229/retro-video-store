from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String) 
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos = db.relationship("Video", secondary="rental", back_populates="customers")

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone
            # "register_at": customer.register_at
            # "videos_checked_out_count": customer.videos_checked_out_count
        }
    
    @classmethod
    def from_dict(cls, data):
        pass
    
    