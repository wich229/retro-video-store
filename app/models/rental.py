from app import db
import datetime

class Rental(db.Model):
    __tablename__ = "rental"
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    # status - track for check_in or check_out
    status = db.Column(db.String) 
    
    
    
    def to_dict(self):
        rental_dict =  {
            "video_id": self.video_id,
            "customer_id": self.customer_id,
            "due_date": self.due_date,
            "status": self.status
        }
        
        return rental_dict
        
        
    
    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
                        video_id = rental_data["video_id"],
                        customer_id = rental_data["customer_id"]
                    )
        
        return new_rental