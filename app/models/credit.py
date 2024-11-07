from app import db
from datetime import datetime

class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    monthly_payment = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # 'salary', 'advance', 'additional'
    is_paid_this_month = db.Column(db.Boolean, default=False)
    is_closed = db.Column(db.Boolean, default=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False)
    transactions = db.relationship('CreditTransaction', backref='credit', lazy=True, 
                                 cascade='all, delete-orphan')