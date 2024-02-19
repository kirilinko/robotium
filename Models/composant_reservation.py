from server import db

class ComposantReservationModel(db.Model):
    __tablename__ = 'composants_reservation'

    id = db.Column(db.Integer, primary_key=True)
    id_composant = db.Column(db.Integer, db.ForeignKey('composants.id'))
    id_reservation = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    composants = db.relationship('ComposantModel', backref='composant', lazy=True)

