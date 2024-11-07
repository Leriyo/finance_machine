from app import db
from datetime import datetime

class CreditTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_id = db.Column(db.Integer, db.ForeignKey('credit.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # 'payment' или 'close'

class SavingTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saving_id = db.Column(db.Integer, db.ForeignKey('saving.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # 'contribution' или 'withdrawal'