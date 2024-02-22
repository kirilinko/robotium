import os
import cv2
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta, time
from flask import session, redirect, url_for, flash

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.split('.')[-1].lower() in allowed_extensions


def upload_image(file):

    FILE_SIZE = 2 * 1024 * 1024

    if file.filename and allowed_file(file.filename):

        if file.content_length < FILE_SIZE:

            filename = secure_filename(file.filename)
            filepath = os.path.join('Fichiers', filename)

            file.save(filepath)

            message = "Image correctement uploader"
            status = True
            path = filepath

        else:
            message = "Le poids de l'image ne doit pas être supérieur à 2Mo"
            status = False
            path = None

    else:
        message = "Vous devez ajouter une image"
        status = False
        path = None

    return {"message": message, "status": status, "path": path}


def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page.', 'warning')
            return redirect(url_for('sing_in'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session.get('user_type') != 'admin':
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
