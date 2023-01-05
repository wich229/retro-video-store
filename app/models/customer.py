from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String) 
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)


    #   {
    #     "id": 1,
    #     "name": "Shelley Rocha",
    #     "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
    #     "postal_code": "24309",
    #     "phone": "(322) 510-8695"
    #   }
    
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
    
    