from server import db
from sqlalchemy import and_
from datetime import datetime, timedelta, time
from sqlalchemy.exc import IntegrityError

class ReservationModel(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    heure_deb = db.Column(db.Time)
    heure_fin = db.Column(db.Time)
    titre = db.Column(db.String())
    descriptions = db.Column(db.String())
    status = db.Column(db.String())
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def approved_reservations(cls):
        return cls.query.filter_by(status="Approuvée").all()

    @classmethod
    def refus_reservations(cls):
        return cls.query.filter_by(status="Refusé").all()

    @classmethod
    def pending_reservations(cls):
        return cls.query.filter_by(status="En revue").all()

    def create(self, id_user):

        currentTime = datetime.utcnow()
        self.heure_deb = datetime.combine(self.date, self.heure_deb)
        self.heure_fin = datetime.combine(self.date, self.heure_fin)
        self.id_user = id_user

        if self.date >= currentTime.date() and (self.heure_fin - self.heure_deb <= timedelta(hours=1)):

            if self.descriptions and len(self.descriptions) > 50:

                if self.titre and len(self.titre) > 5:


                    existing_reservations = ReservationModel.query.filter(
                        and_(
                            ReservationModel.date == self.date,
                            ReservationModel.heure_deb <= self.heure_deb.time(),
                            ReservationModel.heure_fin > self.heure_deb.time()
                        )
                    ).all()


                    if not existing_reservations :

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
                        message = "Votre heure de début est comprise dans l'intervalle de temps d'une réservation prévue pour le même jours."
                        status = False
                else:
                    message = "Le titre doit contenir au moin 5 caractères"
                    status = False
            else:
                message = "La description doit faire au minimum 50 caractères"
                status = False

        else:
            message = "La date de début doit être supérieur à celle du jour et l'intervalle de temps inférieur ou égale à 1h"
            status = False

        return {"message": message, "status": status}

    #Conposant réservé


    @staticmethod
    def verify_date_time(date, heure_deb, heure_fin):
        if date and heure_deb and heure_fin:
            date_reservation = datetime.strptime(date, '%Y-%m-%d').date()
            heure_deb = datetime.strptime(heure_deb, '%H:%M').time()
            heure_fin = datetime.strptime(heure_fin, '%H:%M').time()
            status = True
            message = None
        else:
            status = False
            date_reservation = heure_deb = heure_fin = None
            message = "Tous les champs doivent être remplis"
        return {"date_reservation": date_reservation, "heure_deb": heure_deb, "heure_fin": heure_fin,
                "message": message, "status": status}
