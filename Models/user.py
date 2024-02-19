import re
from server import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    type_user = db.Column(db.String())
    reservations = db.relationship('ReservationModel', backref='user', lazy=True)

    def create(self):

        if self.email and self.validate_email(self.email):

            if self.full_name and 3 < len(self.full_name) < 16:

                if self.password and len(self.password) >= 4:

                    self.password = generate_password_hash(self.password)

                    try:
                        db.session.add(self)
                        db.session.commit()
                        message = "Votre compte a été créé avec succès."
                        status = True

                    except IntegrityError as e:  # Gérer une exception plus spécifique
                        db.session.rollback()
                        message = f"Une erreur d'intégrité est survenue lors de la création de l'utilisateur : {e}"
                        status = False

                    except Exception as e:
                        db.session.rollback()  # Annule les modifications en cas d'erreur.
                        message = f"Une erreur est survenue lors de la création de l'utilisateur : {e}"
                        status = False

                else:
                    message = "Votre mot de passe doit contenir au moins 4 caractères."
                    status = False

            else:
                message = "Votre nom complet doit être compris entre 3 et 15 caractères."
                status = False

        else:
            message = "Adresse mail vide ou format incorrect"
            status = False

        return {"message": message, "status": status}

    # Liste des réservation d'un utilisateur

    def get_reservation(self):

        return self.reservations

    # Connexion d'un utilisateur

    @staticmethod
    def validate_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False


    @staticmethod
    def login(email, password):
        try:
            user = UserModel.query.filter_by(email=email).one()

            if user and check_password_hash(user.password, password):
                message = "Connexion effectuée avec succès"
                status = True
                user_id = user.id
                user_type = user.type_user
            else:
                message = "Identifiant de connexion incorrect"
                status = False
                user_id = user_type = None

        except NoResultFound:
            message = "Utilisateur inexistant"
            status = False
            user_id = user_type = None

        return {"message": message, "status": status, "user_id": user_id, 'user_type': user_type}




