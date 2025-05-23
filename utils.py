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
        'total_patients': len(User.get_patients()),
        'todays_appointments': len(Appointment.get_today()),
        'total_appointments': len(Appointment.get_all()),
        'pending_payments': len([p for p in Payment.get_all() if p.status == 'pending']),
        'total_revenue': sum(p.amount for p in Payment.get_all() if p.status == 'paid')
    }
    return stats
