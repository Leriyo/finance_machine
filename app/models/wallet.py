from app import db
from datetime import datetime

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    incomes = db.relationship('Income', backref='wallet', lazy=True, cascade='all, delete-orphan')
    credits = db.relationship('Credit', backref='wallet', lazy=True, cascade='all, delete-orphan')
    savings = db.relationship('Saving', backref='wallet', lazy=True, cascade='all, delete-orphan')