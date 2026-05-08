from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    # Customization & Monetization
    credits = db.Column(db.Integer, default=10)
    tier = db.Column(db.String(20), default='Free')
    company_name = db.Column(db.String(50), default='Nexus AI')
    theme_color = db.Column(db.String(20), default='#2f81f7')
    
    datasets = db.relationship('Dataset', backref='owner', lazy=True)
    reports = db.relationship('AnalysisReport', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}', '{self.is_approved}', '{self.is_blocked}')"

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reports = db.relationship('AnalysisReport', backref='source_dataset', lazy=True)

class AnalysisReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Completed')
    rows_processed = db.Column(db.Integer, default=0)
    insights_found = db.Column(db.Integer, default=0)
    
    report_content = db.Column(db.Text, nullable=True)
    insights_content = db.Column(db.Text, nullable=True) # Stored individually, maybe JSON
    recommendations_content = db.Column(db.Text, nullable=True)
    
    chart_path = db.Column(db.String(100), nullable=True)
    # Memory and Chat context
    memory_context = db.Column(db.Text, nullable=True)
    
    # Tech Company Upgrades
    forecast_data = db.Column(db.Text, nullable=True)
    alerts_data = db.Column(db.Text, nullable=True)
    
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"AnalysisReport('{self.filename}', '{self.date_posted}', '{self.status}')"
