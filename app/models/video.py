from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)


    #   {
    #     "id": 1,
    #     "title": "Blacksmith Of The Banished",
    #     "release_date": "1979-01-18",
    #     "total_inventory": 10
    #   }
    
    def to_dict(self):
        pass
    
    @classmethod
    def from_dict(cls, data):
        pass