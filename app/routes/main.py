from flask import Blueprint, render_template, jsonify, session, request, redirect, url_for, flash
from app.models.wallet import Wallet
from app.utils.statistics import calculate_statistics

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    selected_wallet_id = session.get('selected_wallet_id')
    return render_template('main.html', 
                         wallets=wallets, 
                         selected_wallet_id=selected_wallet_id)

@bp.route('/select-wallet', methods=['POST'])
def select_wallet():
    wallet_id = request.form.get('wallet_id')
    if wallet_id:
        session['selected_wallet_id'] = int(wallet_id)
        flash('Кошелек успешно выбран', 'success')
    else:
        session.pop('selected_wallet_id', None)
        flash('Кошелек не выбран', 'warning')
    return redirect(url_for('main.index'))

@bp.route('/api/statistics/<int:wallet_id>')
def get_statistics(wallet_id):
    try:
        stats = calculate_statistics(wallet_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500