from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    """Decorator to require patient role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'patient':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def format_currency(amount):
    """Format amount as currency"""
    return f"R$ {amount:,.2f}"

def get_dashboard_stats():
    """Get dashboard statistics for admin"""
    from models import User, Appointment, Payment
    from datetime import date
    
    stats = {
        'total_patients': User.query.filter_by(role='patient').count(),
        'todays_appointments': Appointment.query.filter_by(date=date.today()).count(),
        'total_appointments': Appointment.query.count(),
        'pending_payments': Payment.query.filter_by(status='pending').count(),
        'total_revenue': sum(p.amount for p in Payment.query.filter_by(status='paid').all())
    }
    return stats
