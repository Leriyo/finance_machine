from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.savings import Saving
from app.models.wallet import Wallet
from app.models.transactions import SavingTransaction

bp = Blueprint('savings', __name__, url_prefix='/savings')

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    selected_wallet_id = session.get('selected_wallet_id')
    
    savings = []
    if selected_wallet_id:
        savings = Saving.query.filter_by(wallet_id=selected_wallet_id).all()
    
    return render_template('savings.html', 
                         wallets=wallets,
                         selected_wallet_id=selected_wallet_id,
                         savings=savings)

@bp.route('/add', methods=['POST'])
def add():
    try:
        wallet_id = request.form.get('wallet_id') or session.get('selected_wallet_id')
        if not wallet_id:
            flash('Пожалуйста, выберите кошелек', 'warning')
            return redirect(url_for('savings.index'))

        saving = Saving(
            name=request.form['name'],
            target_amount=float(request.form['target_amount']),
            payment_amount=float(request.form['payment_amount']),
            payment_type=request.form['payment_type'],
            wallet_id=wallet_id,
            current_amount=0
        )
        db.session.add(saving)
        db.session.commit()
        flash('Копилка успешно с��здана', 'success')
    except Exception as e:
        flash(f'Ошибка при создании копилки: {str(e)}', 'error')
    return redirect(url_for('savings.index'))

@bp.route('/contribute/<int:id>', methods=['POST'])
def contribute(id):
    saving = Saving.query.get_or_404(id)
    if not saving.is_paid_this_month:
        saving.current_amount += saving.payment_amount
        saving.is_paid_this_month = True
        
        # Добавляем транзакцию
        transaction = SavingTransaction(
            saving_id=saving.id,
            amount=saving.payment_amount,
            type='contribution'
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Платеж в копилку выполнен', 'success')
    else:
        flash('Платеж в этом месяце уже был выполнен', 'warning')
    return redirect(url_for('savings.index'))

@bp.route('/withdraw/<int:id>', methods=['POST'])
def withdraw(id):
    saving = Saving.query.get_or_404(id)
    withdrawn_amount = saving.current_amount
    saving.current_amount = 0
    saving.is_paid_this_month = False
    
    # Добавляем транзакцию снятия
    transaction = SavingTransaction(
        saving_id=saving.id,
        amount=withdrawn_amount,
        type='withdrawal'
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Средства сняты с копилки', 'success')
    return redirect(url_for('savings.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        saving = Saving.query.get_or_404(id)
        db.session.delete(saving)
        db.session.commit()
        flash('Копилка успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении копилки: {str(e)}', 'danger')
    return redirect(url_for('savings.index'))

@bp.route('/history/<int:id>')
def history(id):
    saving = Saving.query.get_or_404(id)
    transactions = SavingTransaction.query.filter_by(saving_id=id)\
                                        .order_by(SavingTransaction.date.desc()).all()
    return render_template('saving_history.html', saving=saving, transactions=transactions) 