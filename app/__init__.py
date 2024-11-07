from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Импортируем модели
    from app.models.wallet import Wallet
    from app.models.income import Income
    from app.models.credit import Credit
    from app.models.savings import Saving
    from app.models.transactions import CreditTransaction, SavingTransaction
    
    # Регистрируем маршруты
    from app.routes import main, wallet, income, credit, savings
    app.register_blueprint(main.bp)
    app.register_blueprint(wallet.bp)
    app.register_blueprint(income.bp)
    app.register_blueprint(credit.bp)
    app.register_blueprint(savings.bp)
    
    return app 