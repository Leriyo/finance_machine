from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.wallet import Wallet

bp = Blueprint('wallet', __name__, url_prefix='/wallet')

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    return render_template('wallet.html', wallets=wallets)

@bp.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    if name:
        wallet = Wallet(name=name)
        db.session.add(wallet)
        db.session.commit()
        flash('Кошелек успешно создан', 'success')
    return redirect(url_for('wallet.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    wallet = Wallet.query.get_or_404(id)
    db.session.delete(wallet)
    db.session.commit()
    flash('Кошелек удален', 'success')
    return redirect(url_for('wallet.index')) 