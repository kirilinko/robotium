from server import db

class ComposantModel(db.Model):
    __tablename__ = 'composants'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    image_path = db.Column(db.String())
