from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import User, Professional, Appointment, TreatmentPlan, TreatmentStep, Payment
from forms import ProfessionalForm, AppointmentForm, TreatmentPlanForm, TreatmentStepForm, PaymentForm
from utils import admin_required, get_dashboard_stats

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = get_dashboard_stats()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_appointments=recent_appointments)

@admin_bp.route('/patients')
@login_required
@admin_required
def patients():
    patients = User.query.filter_by(role='patient').all()
    return render_template('admin/patients.html', patients=patients)

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

@admin_bp.route('/professionals', methods=['GET', 'POST'])
@login_required
@admin_required
def professionals():
    form = ProfessionalForm()
    
    if form.validate_on_submit():
        professional = Professional(
            name=form.name.data,
            cro=form.cro.data,
            specialty=form.specialty.data
        )
        professional.phone = form.phone.data
        professional.email = form.email.data
        professional.save()
        flash('Professional added successfully!', 'success')
        return redirect(url_for('admin.professionals'))
    
    professionals = Professional.get_all()
    return render_template('admin/professionals.html', professionals=professionals, form=form)

@admin_bp.route('/professional/<int:professional_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_professional(professional_id):
    professional = Professional.get(professional_id)
    if professional:
        professional.delete()
        flash('Professional deleted successfully!', 'success')
    else:
        flash('Professional not found.', 'error')
    return redirect(url_for('admin.professionals'))

@admin_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
@admin_required
def appointments():
    form = AppointmentForm()
    
    # Populate form choices
    patients = User.get_patients()
    professionals = Professional.get_all()
    form.patient_id.choices = [(p.id, p.name) for p in patients]
    form.professional_id.choices = [(p.id, f"{p.name} - {p.specialty}") for p in professionals]
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            professional_id=form.professional_id.data,
            date=form.date.data,
            time=form.time.data
        )
        appointment.notes = form.notes.data
        appointment.status = form.status.data
        appointment.save()
        flash('Appointment created successfully!', 'success')
        return redirect(url_for('admin.appointments'))
    
    appointments = sorted(Appointment.get_all(), key=lambda x: (x.date, x.time), reverse=True)
    return render_template('admin/appointments.html', appointments=appointments, form=form)

@admin_bp.route('/appointment/<int:appointment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_appointment(appointment_id):
    appointment = Appointment.get(appointment_id)
    if appointment:
        appointment.delete()
        flash('Appointment deleted successfully!', 'success')
    else:
        flash('Appointment not found.', 'error')
    return redirect(url_for('admin.appointments'))

@admin_bp.route('/treatment-plans', methods=['GET', 'POST'])
@login_required
@admin_required
def treatment_plans():
    form = TreatmentPlanForm()
    
    # Populate form choices
    patients = User.get_patients()
    form.patient_id.choices = [(p.id, p.name) for p in patients]
    
    if form.validate_on_submit():
        plan = TreatmentPlan(
            patient_id=form.patient_id.data,
            name=form.name.data,
            description=form.description.data
        )
        plan.save()
        flash('Treatment plan created successfully!', 'success')
        return redirect(url_for('admin.treatment_plans'))
    
    plans = TreatmentPlan.get_all()
    return render_template('admin/treatment_plans.html', plans=plans, form=form)

@admin_bp.route('/treatment-plan/<int:plan_id>')
@login_required
@admin_required
def treatment_plan_detail(plan_id):
    plan = TreatmentPlan.get(plan_id)
    if not plan:
        flash('Treatment plan not found.', 'error')
        return redirect(url_for('admin.treatment_plans'))
    
    step_form = TreatmentStepForm()
    step_form.plan_id.data = plan_id
    
    if step_form.validate_on_submit():
        step = TreatmentStep(
            plan_id=plan_id,
            description=step_form.description.data,
            expected_date=step_form.expected_date.data
        )
        step.save()
        flash('Treatment step added successfully!', 'success')
        return redirect(url_for('admin.treatment_plan_detail', plan_id=plan_id))
    
    return render_template('admin/treatment_plan_detail.html', plan=plan, step_form=step_form)

@admin_bp.route('/treatment-step/<int:step_id>/complete', methods=['POST'])
@login_required
@admin_required
def complete_treatment_step(step_id):
    step = TreatmentStep.get(step_id)
    if step:
        step.complete()
        flash('Treatment step marked as completed!', 'success')
        return redirect(url_for('admin.treatment_plan_detail', plan_id=step.plan_id))
    else:
        flash('Treatment step not found.', 'error')
        return redirect(url_for('admin.treatment_plans'))

@admin_bp.route('/payments', methods=['GET', 'POST'])
@login_required
@admin_required
def payments():
    form = PaymentForm()
    
    # Populate form choices
    patients = User.get_patients()
    form.patient_id.choices = [(p.id, p.name) for p in patients]
    
    if form.validate_on_submit():
        payment = Payment(
            patient_id=form.patient_id.data,
            amount=form.amount.data,
            description=form.description.data
        )
        payment.due_date = form.due_date.data
        payment.status = form.status.data
        payment.save()
        flash('Payment record created successfully!', 'success')
        return redirect(url_for('admin.payments'))
    
    payments = sorted(Payment.get_all(), key=lambda x: x.created_at, reverse=True)
    return render_template('admin/payments.html', payments=payments, form=form)

@admin_bp.route('/payment/<int:payment_id>/mark-paid', methods=['POST'])
@login_required
@admin_required
def mark_payment_paid(payment_id):
    payment = Payment.get(payment_id)
    if payment:
        payment.mark_paid()
        flash('Payment marked as paid!', 'success')
    else:
        flash('Payment not found.', 'error')
    return redirect(url_for('admin.payments'))
