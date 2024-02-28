import os
import cv2
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta, time
from flask import session, redirect, url_for, flash

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.split('.')[-1].lower() in allowed_extensions


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


def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' in session and session.get('user_type') == 'admin':
            return redirect(url_for('admin_reservations'))
        elif 'user_type' in session and session.get('user_type') == 'user':
            return redirect(url_for('reservations'))
        return f(*args, **kwargs)
    return decorated_function