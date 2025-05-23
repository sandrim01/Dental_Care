from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='patient')  # admin, patient, dentist, receptionist
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    treatment_plans = db.relationship('TreatmentPlan', backref='patient', lazy=True)
    payments = db.relationship('Payment', backref='patient', lazy=True)
    file_uploads = db.relationship('FileUpload', backref='patient', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_patients():
        return User.query.filter_by(role='patient').all()

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cro = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='professional', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get_today():
        today = date.today()
        return Appointment.query.filter_by(date=today).all()
    
    @staticmethod
    def get_by_patient(patient_id):
        return Appointment.query.filter_by(patient_id=patient_id).all()

class TreatmentPlan(db.Model):
    __tablename__ = 'treatment_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    steps = db.relationship('TreatmentStep', backref='plan', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def get_by_patient(patient_id):
        return TreatmentPlan.query.filter_by(patient_id=patient_id).all()

class TreatmentStep(db.Model):
    __tablename__ = 'treatment_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('treatment_plans.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    expected_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def complete(self):
        self.completed = True
        self.completed_date = date.today()
        db.session.commit()
    
    @staticmethod
    def get_by_plan(plan_id):
        return TreatmentStep.query.filter_by(plan_id=plan_id).all()

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def mark_paid(self):
        self.status = 'paid'
        db.session.commit()
    
    @staticmethod
    def get_by_patient(patient_id):
        return Payment.query.filter_by(patient_id=patient_id).all()

class FileUpload(db.Model):
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), default='document')  # document, xray, photo
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get_by_patient(patient_id):
        return FileUpload.query.filter_by(patient_id=patient_id).all()