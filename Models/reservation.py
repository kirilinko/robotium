from server import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class ReservationModel(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    date_deb = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    description = db.Column(db.String())
    schemas_board = db.Column(db.String())
    status = db.Column(db.String())
    information = db.Column(db.String())
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    composants_reservation = db.relationship('ComposantReservationModel', backref='reservation', lazy=True)

    def create(self):

        if self.date_deb < datetime.utcnow() and self.date_deb < self.date_fin:

            if self.description and len(self.description) > 50:

                try:
                    db.session.add(self)
                    db.session.commit()
                    message = "Réservation éffectuée avec succès"
                    status = True

                except IntegrityError as e:
                    db.session.rollback()
                    message = f"Un erreur liée  à l'intégrité de la base de donnée {e}"
                    status = False

                except Exception as e:
                    db.session.rollback()
                    message = f" Une erreur est survenue lors de la création de la réservation {e}"
                    status = False

            else:
                message = "La description doit faire au minimum 50 caractères"
                status = False

        else:
            message = "La date de début doit être supérieur à celle du jour et inférieur  à la date de fin"
            status = False

        return {"message": message, "status": status}

    #Conposant réservé

    def get_composants_reservation(self):

        return self.composants_reservation

