from app import db
from datetime import datetime

class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    payment_amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # 'salary', 'advance', 'additional'
    is_paid_this_month = db.Column(db.Boolean, default=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False)
    transactions = db.relationship('SavingTransaction', backref='saving', lazy=True, 
                                 cascade='all, delete-orphan')