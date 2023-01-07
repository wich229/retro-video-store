from app import db

class Rental(db.Model):

    __tablename__ = "rental"
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String) 
    
    
    
    def to_dict(self):
        return {
            "video_id": self.video_id,
            "customer_id": self.customer_id,
            "due_date": self.due_date,
            "status": self.status
        }
        
    
    @classmethod
    def from_dict(cls, data):
        pass
    

