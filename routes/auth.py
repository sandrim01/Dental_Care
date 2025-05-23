from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm, RegisterForm
from database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('patient.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('patient.dashboard'))
            else:
                flash('Email ou senha inválidos.', 'error')
        else:
            flash('Por favor, preencha todos os campos.', 'error')
    
    form = LoginForm()
    return render_template('auth/simple_login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        if name and email and password:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email já cadastrado. Use um email diferente.', 'error')
            else:
                # Create new user
                user = User(
                    name=name,
                    email=email,
                    role='patient'
                )
                user.set_password(password)
                if phone:
                    user.phone = phone
                
                db.session.add(user)
                db.session.commit()
                
                flash('Cadastro realizado com sucesso! Faça login.', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
    
    form = RegisterForm()
    
    return render_template('auth/simple_register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('main.index'))
