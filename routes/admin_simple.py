from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import User, Professional, Appointment, TreatmentPlan, TreatmentStep, Payment
from utils import admin_required
from database import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Stats simples
    stats = {
        'total_patients': User.query.filter_by(role='patient').count(),
        'todays_appointments': 0,  # Simplificado por enquanto
        'total_appointments': Appointment.query.count(),
        'pending_payments': Payment.query.filter_by(status='pending').count(),
        'total_revenue': 0  # Simplificado por enquanto
    }
    
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_appointments=recent_appointments)

@admin_bp.route('/patients')
@login_required
@admin_required
def patients():
    patients = User.query.filter_by(role='patient').all()
    return render_template('admin/patients.html', patients=patients)

@admin_bp.route('/appointments')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.all()
    return render_template('admin/appointments.html', appointments=appointments)

@admin_bp.route('/professionals')
@login_required
@admin_required
def professionals():
    professionals = Professional.query.all()
    return render_template('admin/professionals.html', professionals=professionals)

@admin_bp.route('/treatment_plans')
@login_required
@admin_required
def treatment_plans():
    treatment_plans = TreatmentPlan.query.all()
    return render_template('admin/treatment_plans.html', treatment_plans=treatment_plans)

@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    payments = Payment.query.all()
    return render_template('admin/payments.html', payments=payments)

@admin_bp.route('/patient/<int:patient_id>')
@login_required
@admin_required
def patient_detail(patient_id):
    patient = User.query.get(patient_id)
    if not patient or patient.role != 'patient':
        flash('Paciente não encontrado.', 'error')
        return redirect(url_for('admin.patients'))
    
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    treatment_plans = TreatmentPlan.query.filter_by(patient_id=patient_id).all()
    payments = Payment.query.filter_by(patient_id=patient_id).all()
    
    return render_template('admin/patient_detail.html',
                         patient=patient,
                         appointments=appointments,
                         treatment_plans=treatment_plans,
                         payments=payments)