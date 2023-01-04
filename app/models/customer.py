from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)





    #   {
    #     "id": 1,
    #     "name": "Shelley Rocha",
    #     "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
    #     "postal_code": "24309",
    #     "phone": "(322) 510-8695"
    #   }
    
    def to_dict(self):
        pass
    
    @classmethod
    def from_dict(cls, data):
        pass