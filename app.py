import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CSRF protection
csrf = CSRFProtect(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Import models to register them
from models import User, Professional, Appointment, TreatmentPlan, TreatmentStep, Payment, FileUpload

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Register blueprints
from routes.main import main_bp
from routes.auth import auth_bp
from routes.patient import patient_bp
from routes.admin import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Create default admin user if none exists
with app.app_context():
    if not User.get_by_email('admin@clinic.com'):
        admin_user = User(
            name='Administrator',
            email='admin@clinic.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Create sample professionals
        dentist1 = Professional(
            name='Dr. Maria Silva',
            cro='12345-SP',
            specialty='Ortodontia'
        )
        dentist1.save()
        
        dentist2 = Professional(
            name='Dr. João Santos',
            cro='67890-SP',
            specialty='Implantodontia'
        )
        dentist2.save()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
