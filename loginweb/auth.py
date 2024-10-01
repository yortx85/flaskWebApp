from flask import Blueprint, render_template, request, flash, redirect, url_for
from loginweb.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from loginweb import db, app
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect(url_for('auth.acceso'))

@auth.route('/acceder', methods=['GET', 'POST'])
def acceso():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Inicio de sesión correcto.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta.', category='error')
        else:
            flash('La cuenta no existe', category='error')
    return render_template("/acceder.html", user=current_user)

@auth.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Esta cuenta de correo electrónico ya existe', category='error')
        elif len(email) < 4:
            flash('La dirección de correo electrónico debe ser mayor a 3 caracteres', category='error')
        elif len(nombre) < 2:
            flash('El nombre debe ser mayor a 1 caracteres', category='error')
        elif len(apellidos) < 2:
            flash('Los apellidos deben ser mayor a 1 caracteres', category='error')
        elif password1 != password2:
            flash('Las contraseñan no coinciden', category='error')
        elif len(password1) < 7:
            flash('La contraseña debe ser mayor a 7 caracteres', category='error')
        else:
            new_user = User(email=email, nombre=nombre, apellidos=apellidos, password=generate_password_hash(password1, method='scrypt', salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Cuenta creada correctamente', category='success')
            return redirect(url_for('views.home'))

    return render_template("/registrarse.html", user=current_user)

with app.app_context():
    db.create_all()