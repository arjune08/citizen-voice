# =============================================
# WardPulse AI - Flask Application Factory
# =============================================
# Main application setup, configuration, and initialization
# Includes: Flask-Login, Flask-Mail, CSRF, CLI commands

import os
import click
from datetime import datetime
from flask import Flask, redirect, url_for, flash, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import database and models
from models import db, User, Admin

# =============================================
# Flask Extensions (initialized globally)
# =============================================
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # =============================================
    # Configuration
    # =============================================
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'wardpulse-dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # File upload configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

    # Email configuration (Gmail SMTP)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'noreply@wardpulse.ai')
    app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER', 'band@bloodbank.live')

    # Gemini AI API Key
    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', '')

    # =============================================
    # Initialize Extensions
    # =============================================
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # =============================================
    # User Loader for Flask-Login
    # =============================================
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from session - checks both User and Admin tables.
        We prefix admin IDs with 'admin_' to distinguish them."""
        if isinstance(user_id, str) and user_id.startswith('admin_'):
            admin_id = int(user_id.replace('admin_', ''))
            return Admin.query.get(admin_id)
        return User.query.get(int(user_id))

    # =============================================
    # Create Upload Directory
    # =============================================
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # =============================================
    # Register Blueprints
    # =============================================
    from routes import auth_bp, main_bp, user_bp, admin_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # =============================================
    # Template Context Processors
    # =============================================
    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates"""
        return {
            'current_year': datetime.utcnow().year,
            'app_name': 'WardPulse AI',
            'categories': [
                'Road Damage', 'Garbage', 'Street Light', 'Drainage',
                'Water Leakage', 'Electricity', 'Public Safety', 'Tree Fallen', 'Others'
            ],
            'statuses': ['pending', 'verified', 'assigned', 'resolved', 'rejected'],
            'priorities': ['critical', 'high', 'medium', 'low']
        }

    # =============================================
    # Error Handlers
    # =============================================
    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for('main.landing'))

    @app.errorhandler(413)
    def too_large(e):
        flash('File too large. Maximum size is 16MB.', 'error')
        return redirect(request.referrer or url_for('main.landing'))

    # =============================================
    # Create Database Tables
    # =============================================
    with app.app_context():
        db.create_all()

    # =============================================
    # CLI Commands
    # =============================================
    @app.cli.command('create-superadmin')
    @click.option('--name', prompt='Full Name', help='Admin full name')
    @click.option('--email', prompt='Email', help='Admin email')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
    def create_superadmin(name, email, password):
        """Create a Super Admin account via CLI"""
        # Check if admin with this email already exists
        existing = Admin.query.filter_by(email=email).first()
        if existing:
            click.echo(f'Error: Admin with email {email} already exists.')
            return

        admin = Admin(
            full_name=name,
            email=email,
            role='super_admin'
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Super Admin "{name}" created successfully!')

    return app


# =============================================
# Run Application
# =============================================
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
