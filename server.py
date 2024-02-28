import os
import subprocess
import pytz
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, time
from utils import generate_frames, login_required, admin_required, is_login
from flask import Flask, render_template, jsonify, request, Response, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Franck2024'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1999@localhost:5432/flasktest"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
tz_cotonou = pytz.timezone('Africa/Porto-Novo')

from Models import user as user_model, reservation as reservation_model


@app.route("/")
def index():

    return render_template('index.html')


@app.route("/inscription", methods=['POST', 'GET'])
@is_login
def sing_up():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = user_model.UserModel(full_name=full_name, email=email, password=password, type_user='user')
        result = new_user.create()

        return render_template('sing_up.html', data=result)

    if request.method == 'GET':
        return render_template('sing_up.html')


@app.route("/connexion", methods=['POST', 'GET'])
@is_login
def sing_in():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        result = user_model.UserModel.login(email, password)
        print(result)
        # check the authentication state and redirect to user or admin dashboard

        if result['status'] is True:

            session['user_id'] = result['user_id']
            session['user_type'] = result['user_type']

            if result['user_type'] == 'admin':
                return redirect(url_for('admin_reservations'))
            else:
                return redirect(url_for('reservations'))
        else:
            return render_template('sing_in.html', data=result)

    if request.method == 'GET':
        return render_template('sing_in.html')


@app.route("/create/admin", methods=['GET'])
def create_admin():

    new_user = user_model.UserModel(full_name="Admin Robotium", email="admin@robotium.com", password="00000000", type_user='admin')
    result = new_user.create()
    return ("Admin email : admin@robotium.com | mot de passe : 00000000")


@app.route('/deconnexion', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('sing_in'))


@app.route("/user/reservations/new", methods=['POST', 'GET'])
@login_required
def new_reservations():
    if request.method == "GET":
        return render_template('user/makeReservation.html')

    if request.method == "POST":

        titre = request.form.get('titre')
        date_reservation = request.form.get('date')
        heure_deb = request.form.get('heure_deb')
        heure_fin = request.form.get('heure_fin')
        descriptions = request.form.get('descriptions')

        result = reservation_model.ReservationModel.verify_date_time(date_reservation, heure_deb, heure_fin)

        if result['status'] is True:

            new_reservation = reservation_model.ReservationModel(date=result['date_reservation'], heure_deb=result['heure_deb'], heure_fin=result['heure_fin'], titre=titre, descriptions=descriptions, schemas_board=" ", status="En revue", information="")
            result = new_reservation.create(session['user_id'])

            if result['status'] is True:
                return redirect(url_for('reservations'))
            else:
                return render_template('user/makeReservation.html', data=result)
        else:
            return render_template('user/makeReservation.html', data=result)


@app.route("/user/reservations", methods=['GET'])
@login_required
def reservations():
    tz_cotonou = pytz.timezone('Africa/Porto-Novo')
    current_date = datetime.now(tz_cotonou).date()
    current_time = datetime.now(tz_cotonou).strftime('%H:%M:%S')

    login_user = user_model.UserModel.query.filter_by(id=session['user_id']).first()

    traitement =login_user.R_traitement()
    expirer = login_user.R_expirer()
    en_cour= login_user.R_cours()


    return render_template('user/myReservations.html', traitement=traitement,expirer=expirer,en_cour=en_cour, time_b=current_time,date_b=current_date)


@app.route("/user/reservations/<int:id_reservation>", methods=['GET'])
@login_required
def reservation(id_reservation):

    tz_cotonou = pytz.timezone('Africa/Porto-Novo')
    current_time = datetime.now(tz_cotonou).time()

    reservation_info = reservation_model.ReservationModel.query.filter_by(id=id_reservation, id_user=session['user_id']).first()
    if reservation_info:
        return render_template('user/codeStream.html', data=reservation_info, heure=current_time)
    else:
        return ('Ressource Non accessible'),403


@app.route("/admin/reservations", methods=['GET'])
@login_required
@admin_required
def admin_reservations():
    approuved=reservation_model.ReservationModel.approved_reservations()
    refused = reservation_model.ReservationModel.refus_reservations()
    pending = reservation_model.ReservationModel.pending_reservations()
    return render_template('/admin/reservations.html', approuved=approuved, refused=refused, pending=pending)

@app.route("/admin/reservations/edit/<int:id_reservation>", methods=['POST', 'GET'])
@login_required
@admin_required
def edit(id_reservation):

    reservation_info = reservation_model.ReservationModel.query.filter_by(id=id_reservation).first()

    if reservation_info:

        if request.method == "GET":
            return render_template('admin/reservationEdite.html', data=reservation_info)

        if request.method == "POST":

            status = request.form.get('status')

            if status and status in ['Approuvée','Refusé'] :

                reservation_info.status = status
                db.session.commit()
                return redirect(url_for('admin_reservations'))
            else:
                return render_template('admin/reservationEdite.html', error="Le status doit être Approuvée ou Refusé")


    else:
        return render_template('404.html')


@app.route('/send_code', methods=['POST'])
def send_code():
    code = request.form['code']
    now = datetime.now()
    file_path = f"doc\doc.ino"

    with open(file_path, 'w') as file:
        file.write(code)

    sketch_path = os.path.join(os.getcwd(), file_path)
    print(sketch_path)
    try:
        subprocess.run(['arduino-cli', 'compile', '--upload', file_path, '--port', 'COM6', '--fqbn',
                        'arduino:avr:uno'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return jsonify({"message": "Execution du code", "status": True}), 200
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else 'Erreur sans sortie d\'erreur'
        return jsonify({"message": "Erreur : "+ error_message, "status": False}), 500
    finally:
        os.remove(sketch_path)
        pass

@app.route('/video')
#@login_required
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
