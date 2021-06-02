from weather_app import db



class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer(),nullable=False, primary_key=True)
    name = db.Column(db.VARCHAR(64), nullable=False)
    temperature = db.Column(db.Integer(),nullable=False)
    description = db.Column(db.VARCHAR(64), nullable=False)
    def __repr__(self):
        return f"Weather_mode {self.id}"
