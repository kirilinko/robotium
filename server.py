import os
import datetime
import subprocess
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from utils import generate_frames, upload_image, login_required, admin_required
from flask import Flask, render_template, jsonify, request, Response, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Franck2024'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1999@localhost:5432/flasktest"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Models import user, reservation, composant, composant_reservation


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/inscription", methods=['POST', 'GET'])
def sing_up():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = user.UserModel(full_name=full_name, email=email, password=password, type_user='user')
        result = new_user.create()

        return jsonify(result)

    if request.method == 'GET':
        return render_template('sing_up.html')


@app.route("/connexion", methods=['POST', 'GET'])
def sing_in():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        result = user.UserModel.login(email, password)

        # check the authentication state and redirect to user or admin dashboard

        if result.status is True:

            session['user_id'] = result.user_id
            session['user_type'] = result.user_type

            if result.user_type == 'admin':
                return redirect(url_for('admin_reservations'))
            else:
                return redirect(url_for('reservations'))
        else:
            return render_template('sing_in.html', data=result)

    if request.method == 'GET':
        return render_template('sing_in.html')


@app.route('/deconnexion', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('sing_in'))


@app.route("/user/reservations/new", methods=['POST', 'GET'])
#@login_required
def new_reservations():
    if request.method == "GET":
        return render_template('user/makeReservation.html')

    if request.method == "POST":

        date_deb = request.form.get('date_deb')
        date_fin = request.form.get('date_fin')
        description = request.form.get('description')

        new_reservation = reservation.ReservationModel(date_deb=date_deb, date_fin=date_fin, description=description, schemas_board=" ", status="En traitement", information="")
        result = new_reservation.create()

        if result.status is True:
            return redirect('user/reservations')
        else:
            return render_template('user/makeReservation.html', data=result)


@app.route("/user/reservations", methods=['GET'])
#@login_required
def reservations():
    list_reservation = user.UserModel.reservations
    return render_template('user/myReservations.html', data=list_reservation)


@app.route("/user/reservations/<int:id_reservation>", methods=['GET'])
#@login_required
def reservation(id_reservation):
    #reservation_info = reservation.ReservationModel.query.filter_by(id=id_reservation, id_user=session['user_id']).first()
    #if reservation_info:
     #   return render_template('user/codeStream.html', data=reservation_info)
    #else:
        return render_template('user/codeStream.html')


@app.route("/admin/reservations", methods=['GET'])
#@login_required
#@admin_required
def admin_reservations():
    #all_reservations = reservation.ReservationModel.query.all()
    #return render_template('sing_up.html', data=all_reservations)
    return render_template('/admin/reservations.html')

@app.route("/admin/reservations/edit/<int:id_reservation>", methods=['POST', 'GET'])
#@login_required
#@admin_required
def edit(id_reservation):

    #reservation_info = reservation.ReservationModel.query.filter_by(id=id_reservation)
    #if reservation_info:

        if request.method == "GET":
            #return render_template('admin/reservationEdite.html', data=reservation_info)
            return render_template('admin/reservationEdite.html')


        if request.method == "POST":
            # if is to upload schema_board
            reservation_info = reservation.ReservationModel.query.filter_by(id=id_reservation)
            if request.form.get('btn_schema_board'):
                file = request.files['schema_board']
                result = upload_image(file)

                if result.status is True:

                    reservation_info.schemas_board = result['path']
                    db.session.commit()

                else:
                    return render_template('sing_up.html', data=reservation_info, info=result)

            #if is to edit status reservation
            if request.form.get('btn_status'):
                status = request.form.get('status')
                information = request.form.get('information')

                reservation_info.status = status
                reservation_info.information = information
                db.session.commit()

        return render_template('sing_up.html')

    #else:
     #   return render_template('404.html')


@app.route('/send_code', methods=['POST'])
@login_required
def send_code():
    code = request.data.decode('utf-8')
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{file_name}.ino"

    with open(file_path, 'w') as file:
        file.write(code)

    sketch_path = os.path.join(os.getcwd(), file_path)

    # compile and upload code file with arduino-cli no the board

    try:
        subprocess.run(['arduino-cli', 'compile', '--upload', sketch_path, '--port', 'COM6', '--fqbn',
                        'arduino:avr:uno'], check=True)
        return jsonify({"message": "Code en cours d'execusion", "status": True}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Erreur lors de la soumission du code", "status": False}), 500
    finally:
        os.remove(sketch_path)  # Nettoyer le fichier  créé


@app.route('/video')
#@login_required
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
