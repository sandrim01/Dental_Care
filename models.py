from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory storage for MVP
_users = {}
_professionals = {}
_appointments = {}
_treatment_plans = {}
_treatment_steps = {}
_payments = {}
_file_uploads = {}

# ID counters
_user_id_counter = 1
_professional_id_counter = 1
_appointment_id_counter = 1
_treatment_plan_id_counter = 1
_treatment_step_id_counter = 1
_payment_id_counter = 1
_file_upload_id_counter = 1

class User(UserMixin):
    def __init__(self, name, email, role='patient'):
        global _user_id_counter
        self.id = _user_id_counter
        _user_id_counter += 1
        self.name = name
        self.email = email
        self.password_hash = None
        self.role = role  # admin, patient, dentist, receptionist
        self.phone = ''
        self.address = ''
        self.birth_date = None
        self.created_at = datetime.now()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        _users[self.id] = self
        return self
    
    @staticmethod
    def get(user_id):
        return _users.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        for user in _users.values():
            if user.email == email:
                return user
        return None
    
    @staticmethod
    def get_all():
        return list(_users.values())
    
    @staticmethod
    def get_patients():
        return [user for user in _users.values() if user.role == 'patient']

class Professional:
    def __init__(self, name, cro, specialty):
        global _professional_id_counter
        self.id = _professional_id_counter
        _professional_id_counter += 1
        self.name = name
        self.cro = cro
        self.specialty = specialty
        self.phone = ''
        self.email = ''
        self.created_at = datetime.now()
    
    def save(self):
        _professionals[self.id] = self
        return self
    
    def delete(self):
        if self.id in _professionals:
            del _professionals[self.id]
    
    @staticmethod
    def get(professional_id):
        return _professionals.get(professional_id)
    
    @staticmethod
    def get_all():
        return list(_professionals.values())

class Appointment:
    def __init__(self, patient_id, professional_id, date, time):
        global _appointment_id_counter
        self.id = _appointment_id_counter
        _appointment_id_counter += 1
        self.patient_id = patient_id
        self.professional_id = professional_id
        self.date = date
        self.time = time
        self.status = 'scheduled'  # scheduled, completed, cancelled
        self.notes = ''
        self.created_at = datetime.now()
    
    def save(self):
        _appointments[self.id] = self
        return self
    
    def delete(self):
        if self.id in _appointments:
            del _appointments[self.id]
    
    @property
    def patient(self):
        return User.get(self.patient_id)
    
    @property
    def professional(self):
        return Professional.get(self.professional_id)
    
    @staticmethod
    def get(appointment_id):
        return _appointments.get(appointment_id)
    
    @staticmethod
    def get_all():
        return list(_appointments.values())
    
    @staticmethod
    def get_by_patient(patient_id):
        return [apt for apt in _appointments.values() if apt.patient_id == patient_id]
    
    @staticmethod
    def get_today():
        today = date.today()
        return [apt for apt in _appointments.values() if apt.date == today]

class TreatmentPlan:
    def __init__(self, patient_id, name, description=''):
        global _treatment_plan_id_counter
        self.id = _treatment_plan_id_counter
        _treatment_plan_id_counter += 1
        self.patient_id = patient_id
        self.name = name
        self.description = description
        self.status = 'active'  # active, completed, cancelled
        self.created_at = datetime.now()
    
    def save(self):
        _treatment_plans[self.id] = self
        return self
    
    def delete(self):
        if self.id in _treatment_plans:
            del _treatment_plans[self.id]
        # Delete associated steps
        steps_to_delete = [step_id for step_id, step in _treatment_steps.items() 
                          if step.plan_id == self.id]
        for step_id in steps_to_delete:
            del _treatment_steps[step_id]
    
    @property
    def patient(self):
        return User.get(self.patient_id)
    
    @property
    def steps(self):
        return [step for step in _treatment_steps.values() if step.plan_id == self.id]
    
    @staticmethod
    def get(plan_id):
        return _treatment_plans.get(plan_id)
    
    @staticmethod
    def get_all():
        return list(_treatment_plans.values())
    
    @staticmethod
    def get_by_patient(patient_id):
        return [plan for plan in _treatment_plans.values() if plan.patient_id == patient_id]

class TreatmentStep:
    def __init__(self, plan_id, description, expected_date=None):
        global _treatment_step_id_counter
        self.id = _treatment_step_id_counter
        _treatment_step_id_counter += 1
        self.plan_id = plan_id
        self.description = description
        self.expected_date = expected_date
        self.completed = False
        self.completed_date = None
        self.notes = ''
        self.created_at = datetime.now()
    
    def save(self):
        _treatment_steps[self.id] = self
        return self
    
    def delete(self):
        if self.id in _treatment_steps:
            del _treatment_steps[self.id]
    
    def complete(self):
        self.completed = True
        self.completed_date = datetime.now()
        self.save()
    
    @property
    def plan(self):
        return TreatmentPlan.get(self.plan_id)
    
    @staticmethod
    def get(step_id):
        return _treatment_steps.get(step_id)
    
    @staticmethod
    def get_by_plan(plan_id):
        return [step for step in _treatment_steps.values() if step.plan_id == plan_id]

class Payment:
    def __init__(self, patient_id, amount, description=''):
        global _payment_id_counter
        self.id = _payment_id_counter
        _payment_id_counter += 1
        self.patient_id = patient_id
        self.amount = amount
        self.description = description
        self.status = 'pending'  # pending, paid, overdue
        self.due_date = None
        self.paid_date = None
        self.created_at = datetime.now()
    
    def save(self):
        _payments[self.id] = self
        return self
    
    def delete(self):
        if self.id in _payments:
            del _payments[self.id]
    
    def mark_paid(self):
        self.status = 'paid'
        self.paid_date = datetime.now()
        self.save()
    
    @property
    def patient(self):
        return User.get(self.patient_id)
    
    @staticmethod
    def get(payment_id):
        return _payments.get(payment_id)
    
    @staticmethod
    def get_all():
        return list(_payments.values())
    
    @staticmethod
    def get_by_patient(patient_id):
        return [payment for payment in _payments.values() if payment.patient_id == patient_id]

class FileUpload:
    def __init__(self, patient_id, filename, file_type='document'):
        global _file_upload_id_counter
        self.id = _file_upload_id_counter
        _file_upload_id_counter += 1
        self.patient_id = patient_id
        self.filename = filename
        self.file_type = file_type  # document, xray, photo
        self.url = f'/uploads/{filename}'
        self.created_at = datetime.now()
    
    def save(self):
        _file_uploads[self.id] = self
        return self
    
    def delete(self):
        if self.id in _file_uploads:
            del _file_uploads[self.id]
    
    @property
    def patient(self):
        return User.get(self.patient_id)
    
    @staticmethod
    def get(file_id):
        return _file_uploads.get(file_id)
    
    @staticmethod
    def get_all():
        return list(_file_uploads.values())
    
    @staticmethod
    def get_by_patient(patient_id):
        return [file for file in _file_uploads.values() if file.patient_id == patient_id]
