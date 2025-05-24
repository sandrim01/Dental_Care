import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from database import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure PostgreSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jGOEnSzNyXWkxBdoIQayvcImZlklPSQK@trolley.proxy.rlwy.net:43430/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize SQLAlchemy
db.init_app(app)

# Configure CSRF protection (disabled for now)
# csrf = CSRFProtect(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

# Import models after db initialization
from models import User, Professional, Appointment, TreatmentPlan, TreatmentStep, Payment, FileUpload

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from routes.main import main_bp
from routes.auth import auth_bp
from routes.patient import patient_bp
from routes.admin_simple import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)