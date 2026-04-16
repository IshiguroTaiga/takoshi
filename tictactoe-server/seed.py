from app import create_app, db, bcrypt
from app.models import User

# We name this 'flask_app' so it doesn't clash with the folder named 'app'
flask_app = create_app()

with flask_app.app_context():
    db.create_all()
    
    # Check if admin already exists
    if not User.query.filter_by(username='admin').first():
        hashed_pw = bcrypt.generate_password_hash('ishi123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_pw, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin created: user: admin / pass: ishi123")
    else:
        print("ℹ️ Admin already exists.")