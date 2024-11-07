from app.models.wallet import Wallet
from app.models.income import Income
from app.models.credit import Credit
from app.models.savings import Saving

def calculate_statistics(wallet_id):
    wallet = Wallet.query.get_or_404(wallet_id)
    
    # Расчет доходов
    incomes = Income.query.filter_by(wallet_id=wallet_id).all()
    salary_income = sum(i.amount for i in incomes if i.type == 'salary')
    advance_income = sum(i.amount for i in incomes if i.type == 'advance')
    additional_income = sum(i.amount for i in incomes if i.type == 'additional')
    
    # Расчет расходов по кредитам
    credits = Credit.query.filter_by(wallet_id=wallet_id, is_closed=False).all()
    salary_credit = sum(c.monthly_payment for c in credits if c.payment_type == 'salary')
    advance_credit = sum(c.monthly_payment for c in credits if c.payment_type == 'advance')
    additional_credit = sum(c.monthly_payment for c in credits if c.payment_type == 'additional')
    
    # Расчет накоплений
    savings = Saving.query.filter_by(wallet_id=wallet_id).all()
    salary_savings = sum(s.payment_amount for s in savings if s.payment_type == 'salary')
    advance_savings = sum(s.payment_amount for s in savings if s.payment_type == 'advance')
    additional_savings = sum(s.payment_amount for s in savings if s.payment_type == 'additional')
    
    # Расчет общих показателей
    total_income = salary_income + advance_income + additional_income
    total_expenses = (salary_credit + advance_credit + additional_credit +
                     salary_savings + advance_savings + additional_savings)
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_balance': total_income - total_expenses,
        
        'salary_income': salary_income,
        'salary_expenses': salary_credit + salary_savings,
        'salary_balance': salary_income - (salary_credit + salary_savings),
        
        'advance_income': advance_income,
        'advance_expenses': advance_credit + advance_savings,
        'advance_balance': advance_income - (advance_credit + advance_savings),
        
        'additional_income': additional_income,
        'additional_expenses': additional_credit + additional_savings,
        'additional_balance': additional_income - (additional_credit + additional_savings)
    } 