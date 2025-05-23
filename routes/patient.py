from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Appointment, TreatmentPlan, Payment, FileUpload
from forms import ProfileForm, AppointmentForm
from utils import patient_required

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
@login_required
@patient_required
def dashboard():
    appointments = Appointment.get_by_patient(current_user.id)
    treatment_plans = TreatmentPlan.get_by_patient(current_user.id)
    payments = Payment.get_by_patient(current_user.id)
    files = FileUpload.get_by_patient(current_user.id)
    
    # Get recent appointments (last 5)
    recent_appointments = sorted(appointments, key=lambda x: x.created_at, reverse=True)[:5]
    
    # Get pending payments
    pending_payments = [p for p in payments if p.status == 'pending']
    
    return render_template('patient/dashboard.html',
                         recent_appointments=recent_appointments,
                         treatment_plans=treatment_plans,
                         pending_payments=pending_payments,
                         files=files)

@patient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@patient_required
def profile():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.birth_date = form.birth_date.data
        current_user.save()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient.profile'))
    
    return render_template('patient/profile.html', form=form)

@patient_bp.route('/appointments')
@login_required
@patient_required
def appointments():
    appointments = Appointment.get_by_patient(current_user.id)
    appointments = sorted(appointments, key=lambda x: (x.date, x.time), reverse=True)
    return render_template('patient/appointments.html', appointments=appointments)

@patient_bp.route('/treatment-history')
@login_required
@patient_required
def treatment_history():
    treatment_plans = TreatmentPlan.get_by_patient(current_user.id)
    return render_template('patient/treatment_history.html', treatment_plans=treatment_plans)

@patient_bp.route('/request-appointment', methods=['GET', 'POST'])
@login_required
@patient_required
def request_appointment():
    from models import Professional
    
    form = AppointmentForm()
    professionals = Professional.get_all()
    form.professional_id.choices = [(p.id, f"{p.name} - {p.specialty}") for p in professionals]
    form.patient_id.data = current_user.id
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            professional_id=form.professional_id.data,
            date=form.date.data,
            time=form.time.data
        )
        appointment.notes = form.notes.data
        appointment.save()
        flash('Appointment request submitted successfully!', 'success')
        return redirect(url_for('patient.appointments'))
    
    return render_template('patient/appointments.html', form=form, professionals=professionals)
