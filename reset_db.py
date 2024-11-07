from app import create_app, db

app = create_app()

with app.app_context():
    print("Удаление существующих таблиц...")
    db.drop_all()
    
    print("Создание новых таблиц...")
    db.create_all()
    
    print("База данных успешно пересоздана!") 