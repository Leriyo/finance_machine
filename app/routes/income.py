from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.income import Income
from app.models.wallet import Wallet

bp = Blueprint('income', __name__, url_prefix='/income')

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    selected_wallet_id = session.get('selected_wallet_id')
    
    incomes = []
    if selected_wallet_id:
        incomes = Income.query.filter_by(wallet_id=selected_wallet_id)\
                             .order_by(Income.date.desc()).all()
    
    return render_template('income.html', 
                         wallets=wallets,
                         selected_wallet_id=selected_wallet_id,
                         incomes=incomes)

@bp.route('/add', methods=['POST'])
def add():
    try:
        wallet_id = request.form.get('wallet_id') or session.get('selected_wallet_id')
        if not wallet_id:
            flash('Пожалуйста, выберите кошелек', 'warning')
            return redirect(url_for('income.index'))
            
        amount = request.form.get('amount', type=float)
        income_type = request.form.get('type')
        
        income = Income(
            wallet_id=wallet_id,
            amount=amount,
            type=income_type
        )
        
        db.session.add(income)
        db.session.commit()
        flash('Доход успешно добавлен', 'success')
        
    except Exception as e:
        flash(f'Ошибка при добавлении дохода: {str(e)}', 'danger')
    return redirect(url_for('income.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    income = Income.query.get_or_404(id)
    wallet_id = income.wallet_id
    db.session.delete(income)
    db.session.commit()
    flash('Доход удален', 'success')
    return redirect(url_for('income.index', wallet_id=wallet_id)) 