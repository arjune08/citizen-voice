# =============================================
# WardPulse AI - Flask Application Factory
# =============================================

import os
import click
from datetime import datetime
from flask import Flask, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

from models import db, User, Admin

login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        secret_key = 'dev-only-change-me'
        if not os.environ.get('FLASK_ENV') == 'development':
            app.logger.warning('SECRET_KEY is not set; using a development fallback.')
    app.config['SECRET_KEY'] = secret_key

    database_uri = os.environ.get('DATABASE_URI', 'sqlite:///database.db')
    # Render/Railway commonly expose PostgreSQL as DATABASE_URL.
    if database_uri.startswith('postgres://'):
        database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'webp'}

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'] or 'noreply@citizenvoice.local')
    app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER', '')

    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', '')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        """Load either a citizen or admin from the Flask-Login session."""
        try:
            if isinstance(user_id, str) and user_id.startswith('admin_'):
                return Admin.query.get(int(user_id.replace('admin_', '', 1)))
            return User.query.get(int(user_id))
        except (TypeError, ValueError):
            return None

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from routes import auth_bp, main_bp, user_bp, admin_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_globals():
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

    @app.get('/health')
    def health():
        """Simple deployment health endpoint."""
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'ok', 'service': 'citizen-voice'}), 200
        except Exception:
            app.logger.exception('Health check database failure')
            return jsonify({'status': 'error'}), 503

    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for('main.landing'))

    @app.errorhandler(413)
    def too_large(e):
        flash('File too large. Maximum size is 16MB.', 'error')
        return redirect(request.referrer or url_for('main.landing'))

    with app.app_context():
        db.create_all()

    @app.cli.command('create-superadmin')
    @click.option('--name', prompt='Full Name', help='Admin full name')
    @click.option('--email', prompt='Email', help='Admin email')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
    def create_superadmin(name, email, password):
        """Create a Super Admin account via CLI."""
        existing = Admin.query.filter_by(email=email.strip().lower()).first()
        if existing:
            click.echo(f'Error: Admin with email {email} already exists.')
            return
        admin = Admin(full_name=name.strip(), email=email.strip().lower(), role='super_admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Super Admin "{name}" created successfully!')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=os.environ.get('FLASK_DEBUG', '0') == '1', port=int(os.environ.get('PORT', 5000)))
