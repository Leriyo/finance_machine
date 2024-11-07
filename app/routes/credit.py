from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.credit import Credit
from app.models.wallet import Wallet
from app.models.transactions import CreditTransaction

bp = Blueprint('credit', __name__, url_prefix='/credit')

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    selected_wallet_id = session.get('selected_wallet_id')
    
    credits = []
    if selected_wallet_id:
        credits = Credit.query.filter_by(
            wallet_id=selected_wallet_id,
            is_closed=False
        ).all()
    
    return render_template('credit.html', 
                         wallets=wallets,
                         selected_wallet_id=selected_wallet_id,
                         credits=credits)

@bp.route('/add', methods=['POST'])
def add():
    try:
        wallet_id = request.form.get('wallet_id') or session.get('selected_wallet_id')
        if not wallet_id:
            flash('Пожалуйста, выберите кошелек', 'warning')
            return redirect(url_for('credit.index'))

        credit = Credit(
            name=request.form['name'],
            total_amount=float(request.form['total_amount']),
            monthly_payment=float(request.form['monthly_payment']),
            payment_type=request.form['payment_type'],
            wallet_id=wallet_id,
            remaining_amount=float(request.form['total_amount'])
        )
        db.session.add(credit)
        db.session.commit()
        flash('Кредит успешно добавлен', 'success')
    except Exception as e:
        flash(f'Ошибка при добавлении кредита: {str(e)}', 'error')
    return redirect(url_for('credit.index'))

@bp.route('/pay/<int:id>', methods=['POST'])
def make_payment(id):
    credit = Credit.query.get_or_404(id)
    if not credit.is_paid_this_month:
        credit.remaining_amount -= credit.monthly_payment
        credit.is_paid_this_month = True
        
        # Добавляем транзакцию
        transaction = CreditTransaction(
            credit_id=credit.id,
            amount=credit.monthly_payment,
            type='payment'
        )
        db.session.add(transaction)
        
        if credit.remaining_amount <= 0:
            credit.is_closed = True
            
        db.session.commit()
        flash('Платеж по кредиту выполнен', 'success')
    else:
        flash('Платеж в этом месяце уже был выполнен', 'warning')
    return redirect(url_for('credit.index'))

@bp.route('/close/<int:id>', methods=['POST'])
def close_credit(id):
    credit = Credit.query.get_or_404(id)
    credit.is_closed = True
    
    # Добавляем транзакцию закрытия
    transaction = CreditTransaction(
        credit_id=credit.id,
        amount=credit.remaining_amount,
        type='close'
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Кредит закрыт', 'success')
    return redirect(url_for('credit.index'))

@bp.route('/history/<int:id>')
def history(id):
    credit = Credit.query.get_or_404(id)
    transactions = CreditTransaction.query.filter_by(credit_id=id)\
                                        .order_by(CreditTransaction.date.desc()).all()
    return render_template('credit_history.html', credit=credit, transactions=transactions) 