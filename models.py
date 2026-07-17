# =============================================
# WardPulse AI - Database Models
# =============================================
# All SQLAlchemy models for the application
# Tables: User, Admin, Issue, Vote, Notification

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy instance
db = SQLAlchemy()


# =============================================
# User Model - Citizens who report issues
# =============================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_photo = db.Column(db.String(256), default=None)
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)

    # Relationships
    issues = db.relationship('Issue', backref='reporter', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='voter', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    def get_total_votes_received(self):
        """Get total votes received across all user's issues"""
        total = 0
        for issue in self.issues:
            total += issue.votes_count
        return total

    @property
    def is_active(self):
        return self.is_active_user

    def to_dict(self):
        """Serialize user to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'profile_photo': self.profile_photo,
            'is_active': self.is_active_user,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M') if self.last_login else None,
            'issues_count': self.issues.count(),
            'votes_received': self.get_total_votes_received()
        }

    def __repr__(self):
        return f'<User {self.email}>'


# =============================================
# Admin Model - Ward Officers and Super Admins
# =============================================
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='moderator')
    # Roles: super_admin, ward_officer, moderator
    is_active_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)

    def set_password(self, password):
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.is_active_admin

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'

    def get_id(self):
        """Override to distinguish admin session from citizen user session"""
        return f"admin_{self.id}"


    def to_dict(self):
        """Serialize admin to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active_admin,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M') if self.last_login else None
        }

    def __repr__(self):
        return f'<Admin {self.email} ({self.role})>'


# =============================================
# Issue Model - Civic complaints/issues
# =============================================
class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # Categories: Road Damage, Garbage, Street Light, Drainage,
    #             Water Leakage, Electricity, Public Safety, Tree Fallen, Others
    ward = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String(256), nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='medium')
    # Priority: critical, high, medium, low
    status = db.Column(db.String(20), nullable=False, default='pending')
    # Status: pending, verified, assigned, resolved, rejected
    votes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    votes = db.relationship('Vote', backref='issue', lazy='dynamic', cascade='all, delete-orphan')

    # Valid categories
    CATEGORIES = [
        'Road Damage', 'Garbage', 'Street Light', 'Drainage',
        'Water Leakage', 'Electricity', 'Public Safety', 'Tree Fallen', 'Others'
    ]

    # Valid priorities
    PRIORITIES = ['critical', 'high', 'medium', 'low']

    # Valid statuses
    STATUSES = ['pending', 'verified', 'assigned', 'resolved', 'rejected']

    def has_voted(self, user_id):
        """Check if a user has already voted on this issue"""
        return Vote.query.filter_by(issue_id=self.id, user_id=user_id).first() is not None

    def to_dict(self):
        """Serialize issue to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'ward': self.ward,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_path': self.image_path,
            'priority': self.priority,
            'status': self.status,
            'votes_count': self.votes_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None,
            'user_id': self.user_id,
            'reporter_name': self.reporter.full_name if self.reporter else 'Unknown'
        }

    def __repr__(self):
        return f'<Issue {self.id}: {self.title}>'


# =============================================
# Vote Model - Upvotes on issues
# =============================================
class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent duplicate votes: one vote per user per issue
    __table_args__ = (
        db.UniqueConstraint('issue_id', 'user_id', name='unique_vote'),
    )

    def __repr__(self):
        return f'<Vote user={self.user_id} issue={self.issue_id}>'


# =============================================
# Notification Model - User notifications
# =============================================
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(20), default='info')
    # Types: success, error, info, warning
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Serialize notification to dictionary"""
        return {
            'id': self.id,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

    def __repr__(self):
        return f'<Notification {self.id}: {self.message[:30]}>'
