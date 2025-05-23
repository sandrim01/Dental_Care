from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, DateField, TimeField, DecimalField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from datetime import date

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    birth_date = DateField('Birth Date', validators=[Optional()])

class ProfessionalForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    cro = StringField('CRO Number', validators=[DataRequired(), Length(min=5, max=20)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    email = EmailField('Email', validators=[Optional(), Email()])

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', validators=[DataRequired()], coerce=int)
    professional_id = SelectField('Professional', validators=[DataRequired()], coerce=int)
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    time = TimeField('Time', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')

class TreatmentPlanForm(FlaskForm):
    patient_id = SelectField('Patient', validators=[DataRequired()], coerce=int)
    name = StringField('Treatment Plan Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])

class TreatmentStepForm(FlaskForm):
    plan_id = HiddenField('Plan ID', validators=[DataRequired()])
    description = StringField('Step Description', validators=[DataRequired(), Length(max=500)])
    expected_date = DateField('Expected Date', validators=[Optional()])

class PaymentForm(FlaskForm):
    patient_id = SelectField('Patient', validators=[DataRequired()], coerce=int)
    amount = DecimalField('Amount', validators=[DataRequired()], places=2)
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    due_date = DateField('Due Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ], default='pending')
